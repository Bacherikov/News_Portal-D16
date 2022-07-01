from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache


class Author (models.Model):  # Авторы статей/новостей (далее - постов)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self, new_rating):
        self.rating = new_rating
        self.save()

    def __str__(self):
        return f'Автор: {self.user.username}'


class Category (models.Model):  # Категории постов
    name = models.CharField(max_length=30, unique=True,)
    # Фактически тут автоматом создастся атрибут posts со связью многие-ко-многим с моделью Post

    # поле для хранения подписавшихся на эту категорию пользователей
    subscriptions = models.ManyToManyField(User, related_name='subscribed_categories')

    def __str__(self):
        return f'Категория: {self.name}'


class Post (models.Model):  # Модель поста  (статьи/новости)
    article = 'ar'
    news = 'nw'

    VIEW = [
        (article, 'Статья'),
        (news, 'Новость')
        ]
    # связь один ко многим с моделью Author
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    view = models.CharField(max_length=2, choices=VIEW, default=article)
    create_time = models.DateTimeField(auto_now_add=True)
    # связь «многие ко многим» с моделью Category (через дополнительную модель PostCategory)
    categories = models.ManyToManyField(Category, through='PostCategory', related_name='posts')
    heading = models.CharField(max_length=255)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)

    def get_categories(self):  # D9 п17 для подписки
        result = []
        for category in self.categories.all():
            result.append(category)
        return result

    # def get_comments(self): пока закоментил обязательно  реализовать
    #     result = []
    #     for comment in self.comments.all():
    #         result.append(comment)
    #     return result

    def __str__(self):
        return f'Заголовок: {self.heading.title()}'

    def like(self):
        self.rating_post = + 1
        self.save()

    def dislike(self):
        self.rating_post = - 1
        self.save()

    def preview(self):
        # возвращает начало статьи, длиной в 124 символа и добавляет многоточие
        size = 124 if len(self.text_post) > 124 else len(self.text_post)
        return self.text_post[:size] + "..."

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


# D9.2 Модель реализующая связь Многие ко Многим
class PostCategory (models.Model):  # Модель для связи таблиц Пост и Категории, для организации 3-й формы нормализации
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment (models.Model):  # Комметарии к постам
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment = + 1
        self.save()

    def dislike(self):
        self.rating_comment = - 1
        self.save()