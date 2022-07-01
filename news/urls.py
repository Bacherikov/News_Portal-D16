from django.urls import path
from .views import PostsList, PostDetail, PostsSearchList, PostCreate, PostUpdate, PostDelete, subscription
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path означает "путь".
    path('', cache_page(60 * 5)(PostsList.as_view())),  # Основная страница.
    path('<int:pk>', PostDetail.as_view(), name='post'),  # Вывод по одному объекту
    path('search/', PostsSearchList.as_view(), name='posts_filters'),  # Поиск объектов
    path('add/', PostCreate.as_view(), name='post_create'),  # Создание объектов
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),  # Редактирование объектов
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),  # Удаление объектов
    path('subscription/', subscription, name='subscription'),  # поле подписаться
        ]