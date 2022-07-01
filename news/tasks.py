from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post
from datetime import datetime, timedelta
from collections import defaultdict
from django.utils import timezone


@shared_task
# функция для рассылки писем
def send_posts(email_list, posts):
    print('START TASK send_posts')
    # на случай, если там только один адрес, а не список
    if isinstance(email_list, str):
        subscribers_list = [email_list, ]
    else:
        subscribers_list = email_list

    email_from = settings.DEFAULT_FROM_EMAIL  # в settings должно быть заполнено
    subject = 'В категориях, на которые вы подписаны появились новые статьи'
    text_message = 'В категориях, на которые вы подписаны появились новые статьи'

    # рендерим в строку шаблон письма и передаём туда переменные, которые в нём используем
    render_html_template = render_to_string(
        'send_posts_list.html',
        {'posts': posts,
         'subject': subject
         }
        )

    # формируем письмо
    msg = EmailMultiAlternatives(subject, text_message, email_from, list(subscribers_list))
    # прикрепляем хтмл-шаблон
    msg.attach_alternative(render_html_template, 'text/html')
    # отправляем
    msg.send()
    print('TASK FIFNISHED send_posts')

# задача для рассылки статей за последние 7 дней по почте
# пользователя, которые подписались на категории
@shared_task()
def weekly_mailing():
    # DEBUG
    print('START TASK weekly_mailing')

    # берём посты за последние 7 дней
    # здесь мы получаем queryset
    last_week_posts_qs = Post.objects.filter(create_time__gte=datetime.now(tz=timezone.utc) - timedelta(days=7))

    # собираем в словарь список пользователей и список постов, которые им надо разослать
    posts_for_user = defaultdict(set)  # user -> posts

    for post in last_week_posts_qs:
        for category in post.categories.all():
            for user in category.subscriptions.all():
                posts_for_user[user].add(post)

    # непосредственно рассылка
    for user, posts in posts_for_user.items():
        send_posts(user.email, posts)

        # DEBUG
        print('TASK FIFNISHED weekly_mailing')