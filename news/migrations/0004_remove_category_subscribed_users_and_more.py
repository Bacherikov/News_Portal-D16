from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_alter_post_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subscribed_users',
        ),
        migrations.AddField(
            model_name='category',
            name='subscriptions',
            field=models.ManyToManyField(related_name='subscribed_categories', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='news.author'),
        ),
        migrations.DeleteModel(
            name='SubscribedUsersCategory',
        ),
    ]