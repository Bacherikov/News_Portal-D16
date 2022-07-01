from django_filters import FilterSet, DateFilter, CharFilter
from .models import Post


class PostFilter(FilterSet):
    heading_post = CharFilter(field_name='heading', lookup_expr='icontains', label='Заголовок')
    author_post = CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Имя пользователя(Автор)')
    create_time_post = DateFilter(field_name='create_time', lookup_expr='gte', label='Дата(yyyy-mm-dd)')

    class Meta:
        model = Post

        fields = {

        }