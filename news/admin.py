from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


# D14.5
def nullfy_rating_post(modeladmin, request, queryset):  # все аргументы уже должны быть вам знакомы,
    # самые нужные из них это request — объект хранящий информацию о запросе и
    # queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating_post=0)

nullfy_rating_post.short_description = 'Обнулить рейтинг'  # описание для более понятного представления
# в админ панеле задаётся, как будто это объект


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = [field.name for field in Post._meta.get_fields()]  # Выдает  ошибку из-за
    # ManyToManyField в поле категория
    # генерируем список имён всех полей для более красивого отображения
    list_display = ('author', 'create_time', 'view', 'heading', 'rating_post')
    list_filter = ('author', 'create_time', 'rating_post')
    search_fields = ('author', 'view')
    actions = [nullfy_rating_post]  # добавляем действия в список


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('user', 'rating')
    search_fields = ('user', 'rating')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')
    list_filter = ('post', 'category')
    search_fields = ('post', 'category')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'comment_text', 'create_time', 'rating_comment')
    list_filter = ('post', 'user', 'comment_text', 'create_time', 'rating_comment')
    search_fields = ['user']


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
