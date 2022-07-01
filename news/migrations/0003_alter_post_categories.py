from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_subscribeduserscategory_category_subscribed_users_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(related_name='posts', through='news.PostCategory', to='news.Category'),
        ),
    ]