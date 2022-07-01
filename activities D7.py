# D7_2Проект News Portal
# # Доработайте ваш сайт с новостями:
#
# Задание -Добавьте постраничный вывод на основной странице новостей, чтобы на одной странице было не больше 10новостей,
#     и были видны номера лишь ближайших страниц, а также возможность перехода к первой или последней странице.

# |1|  D7_2 корректно настроим шаблон:
# |постраничный вывод|
# -- настройка APP_DIRS должна быть выставлена в True;
# -- переходим в файл models.py в модели Post меняем функцию __str__
# def __str__(self):
#     return f'{self.heading} {self.text_post[:100]} '
# -- файл шаблона должен лежать в соответствующей папке внутри папки приложения.
# Переходим в файл NewsPaper/news/views.py
# Вписываем и добавляем строку paginate_by = 10 в представление PostsList
# Переходим в файл templates/posts.html
# Добавляем блок пагинации

# Задание-Добавьте страничку /news/search.
#         На ней должна быть реализована возможность пользователя искать новости по определённым критериям.
#
#         Критерии должны быть следующие:
#                 позже какой-либо даты;
#                 по названию;
#                 по имени пользователя автора;
#                 всё вместе.
#
# ВЫПОЛНЕНИЕ Для начала поставим дополнительные пакеты через pip:
# # python -m pip install django-filter
#
# Не забываем вписать ‘django_filters’ в INSTALLED_APPS в настройках, чтобы получить доступ к фильтрам в приложении.
# Теперь надо создать файл filters.py в директории news/ в той же папке, где лежат наши модели.
# Заполняем файл

# Переходим в файл NewsPaper/news/views.py
# Создаем новый класс class PostsSearchList(ListView):
# Добавляем функцию def get_context_data(self, **kwargs):

# Создаем папки news/search в NewsPaper/templates и отдельный файл шаблона posts_filters, для странички search
# Наполняем файл нового шаблона posts_filters
# <!-- Перед таблицей добавим форму для поиска -->
# <!-- Поменяем posts на filter.qs, т.к. теперь мы забираем уже отобранную по каким-то параметрам информацию -->
# Добавляем url для странички /news/search/

# Отредактируем фильтр новостей и сделаем из него более подходящий нам вариант:
# heading_post = CharFilter(field_name='heading', lookup_expr='icontains', label='Заголовок')
# author_post = CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Имя пользователя')
# create_time_post = DateFilter(field_name='create_time', lookup_expr='gte', label='Дата(+)')

# Примеры поиска:
# заголовок - Новость или Статья
# Имя пользователя - ivan или petr
# Дата форма записи - 021-11-28

# Добавим в приложение news файл forms.py.
# Создадим class PostForm(ModelForm):
# Создаем шаблон post_create.html директории templates/news/

# Правим шаблон posts_filters.html:
# - правка заголовков странички, перенос поиска.

# Правим шаблон posts.html:
# -(<a href="{% url 'post' post.id %}">{{ post.heading|truncatewords:2|censor:'***'}}</a>)

# Переходим в views.py создаем дженерик Create и подправляем PostDetail

# Пропишем дополнительные пути в urls.py и дописываем ко всем свои name=

# добавим одну хитрость в наш models.py .
# def get_absolute_url(self):
# добавим абсолютный путь, чтобы после создания переходить на страницу с новостями
# return f'/news/{self.id}'

# Переходим в views.py создаем дженерик Delete, Update

# Добавляем новый шаблон по адресу news/product_delete.html

# Правим шаблон posts.html:
# Добавляем ссылки на редактирование, создание  и удаление на главную страницу и переход на страницу search
# <a href="{% url 'post_update' post.id %}"><u>Редактировать</u></a>
# <a href="{% url 'post_delete' post.id %}"><u> Удалить </u></a>
# <a href="{% url 'post_create' %}">Добавить новый пост</a> <br>
# <a href="search/">| Поиск |</a>

# Прописываем оставшиеся пути в urls.py
# Один из примеров path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

