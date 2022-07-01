
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
# from django.views.generic.edit import CreateView
# from .forms import BaseRegisterForm
from django.contrib.auth.decorators import login_required
from news.models import Author

# class BaseRegisterView(CreateView):
#     model = User
#     form_class = BaseRegisterForm
#     success_url = '/'


@login_required  # 13.8
def upgrade_me(request):
    user = request.user
    if not Author.objects.filter(user=user).exists():
        Author.objects.create(user=user)
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')
