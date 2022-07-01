from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['heading', 'author', 'view', 'categories', 'text_post']