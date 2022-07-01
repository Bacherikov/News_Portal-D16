# для рассылки почты потом перенесем в сигналы
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post, Category


@receiver(post_save, sender=User)
def post_save_post(created, **kwargs):
    # берём объект созданного пользователя
    user_instance = kwargs['instance']
    email_from = settings.DEFAULT_FROM_EMAIL

    # если он создан, а не изменён
    if created:
        subject = 'Приветствуем у нас на портале!'
        text_message = 'Приветственный текст'

        # рендерим в строку шаблон письма и передаём туда переменные, которые в нём используем
        render_html_template = render_to_string('hello_message.html', {'user': user_instance,
                                                                       'subject': subject,
                                                                       'text': text_message})

        # формируем письмо
        msg = EmailMultiAlternatives(subject, text_message, email_from, [user_instance.email, ])
        # прикрепляем хтмл-шаблон
        msg.attach_alternative(render_html_template, 'text/html')
        # отправляем
        msg.send()


# при сохранении объекта модели Пост будет срабатывать этот сигнал
@receiver(post_save, sender=Post)
def post_save_post(created, **kwargs):  # получить параметры можно двумя способами. Первый тут
    # А можно вытащить из kwargs
    # тут вытаскиваем объект только что сохранённого поста
    post_instance = kwargs['instance']

    # собираем почту всех, кто подписался на категории этой статьи
    # множество тут у меня для того, чтобы не было повторений, чтобы несколько раз не приходило одно и то же письмо
    # но на этапе формирования письма надо будет передать именно список
    subscribers_list = {user.email
                        for category in post_instance.categories.all()
                        for user in category.subscriptions.all()}
    email_from = settings.DEFAULT_FROM_EMAIL

    # если статья создана
    if created:
        # отправка письма с превью и ссылкой на статью
        subject = 'В категориях, на которые вы подписаны появилась новая статья'
        text_message = f'В категориях, на которые вы подписаны появилась новая статья:'
    else:
        # отправка письма с ссылкой на статью и помекой об изменении
        subject = 'Приходит с сигнала. В категориях, на которые вы подписаны была изменена статья'
        text_message = f'В категориях, на которые вы подписаны была изменена статья:'

    # рендерим в строку шаблон письма и передаём туда переменные, которые в нём используем
    render_html_template = render_to_string('send_post.html', {'post': post_instance, 'subject': subject})

    # формируем письмо
    msg = EmailMultiAlternatives(subject, text_message, email_from, list(subscribers_list))
    # прикрепляем хтмл-шаблон
    msg.attach_alternative(render_html_template, 'text/html')
    # отправляем
    msg.send()


@receiver(m2m_changed, sender=Post.categories.through)
def notify_managers_posts(instance, action, pk_set, *args, **kwargs):
    if action == 'post_add':
        html_content = render_to_string(
            'post_changes_create.html',
            {'post': instance, }
        )
        for pk in pk_set:
            category = Category.objects.get(pk=pk)
            recipients = [user.email for user in category.subscriptions.all()]
            msg = EmailMultiAlternatives(
                subject=f'На сайте NewsPaper новая статья: {instance.heading}',
                body=f'На сайте NewsPaper новая статья: {instance.heading}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipients
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()