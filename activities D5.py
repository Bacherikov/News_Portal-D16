# python manage.py shell

from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment
import random

# Создание двух пользователей, с заполнением всех обязательных полей
petr_user = User.objects.create_user(username='petr', email='petr_user@mail.ru', password='1111')
ivan_user = User.objects.create_user(username='ivan', email='ivan_user@mail.ru', password='0000')

# Создание двух объектов модели Author
petr = Author.objects.create(user=petr_user)
ivan = Author.objects.create(user=ivan_user)

# Добавлякм 4 категории в модель Category
fishing = Category.objects.create(name='Рыбалка')
construction = Category.objects.create(name='Cтроительство')
programming = Category.objects.create(name='Программирование')
cycling = Category.objects.create(name='Велоспорт')

# Добавлякм две статьи и одну новость в модель Post
article_1_fishing = "Статья №1 в категории  рыбалка от автора Петр"
article_2_construction = "Сатья №2 в категории строительство от автора Иван"
news_1_programming = "Новость №1 в категории программирование от автора Петр"

article_petr = Post.objects.create(author=petr, view=Post.article, heading='Статья №1 в категории  рыбалка от автора Петр', text_post=article_1_fishing)
article_ivan = Post.objects.create(author=ivan, view=Post.article, heading='Статья №2 в категории строительство от автора Иван', text_post=article_2_construction)
news_petr = Post.objects.create(author=petr, view=Post.news, heading='Новость №1 в категории программирование от автора Петр', text_post=news_1_programming)

# Присваиваем им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий)
PostCategory.objects.create(post=article_petr, category=fishing)
PostCategory.objects.create(post=article_petr, category=programming)
PostCategory.objects.create(post=article_ivan, category=construction)
PostCategory.objects.create(post=news_petr, category=cycling)

# Создаем комментарии
comment1 = Comment.objects.create(post=article_petr, user=ivan.user, comment_text='Комментарий №1 от автора Иван к статье №1 в категории  рыбалка от автора Петр')
comment2 = Comment.objects.create(post=article_ivan, user=petr.user, comment_text='Комментарий №2 от автора Петр к статье №2 в категории строительство от автора Иван')
comment3 = Comment.objects.create(post=news_petr, user=ivan.user, comment_text='Комментарий №3 от автора Иван к новости №1 в категории велоспорт от автора Петр')
comment4 = Comment.objects.create(post=news_petr, user=petr.user, comment_text='Комментарий №4 от автора Петр к новости №1 в категории велоспорт от автора Петр')

# Список всех объектов, которые можно лайкать
list_for_like = [article_ivan,
                 article_ivan,
                 news_petr,
                 comment1,
                 comment2,
                 comment3,
                 comment4
                 ]
# 100 рандомных лайков\дислайков (по четности счетчика)
for i in range(100):
    random_odj = random.choice(list_for_like)
    if i % 2:
        random_odj.like()
    else:
        random_odj.dislike()

# Подсчет рейтинга Петр
rating_petr = (sum([Post.rating_post*3 for Post in Post.objects.filter(author=petr)])
             + sum([Comment.rating_comment for Comment in Comment.objects.filter(user=petr.user)])
             + sum([Comment.rating_comment for Comment in Comment.objects.filter(post__author=petr)])
               )

# Обновляем рейтинг
petr.update_rating(rating_petr)

# Подсчет рейтинга Иван
rating_ivan= (sum([Post.rating_post*3 for Post in Post.objects.filter(author=ivan)])
               + sum(Comment.rating_comment for Comment in Comment.objects.filter(user=ivan.user))
               + sum([Comment.rating_comment for Comment in Comment.objects.filter(post__author=ivan)])
               )
ivan.update_rating(rating_ivan)

# лучший автор
best_author = Author.objects.all().order_by('rating')[0]
print("Лудший автор")
print("username:", best_author.user.username)
print("Рейтинг:", best_author.rating)
print("")

# Лучщая статья
best_article = Post.objects.filter(view=Post.article).order_by('-rating_post')[0]
print("Лучшая статья")
print("Дата:", best_article.create_time)
print("Автор:", best_article.author.user.username)
print("Рейтирг:", best_article.author.rating)
print("Загаловок:", best_article.heading)
print("Превью:", best_article.preview())
print("")

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
print("Комментарии к ней")
for Comment in Comment.objects.filter(post=best_article):
    print("Дата:", Comment.create_time)
    print("Автор:", Comment.user.username)
    print("Рейтинг", Comment.rating_comment)
    print("Комментарий", Comment.comment_text)
    print("")