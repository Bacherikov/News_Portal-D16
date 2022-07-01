from django.core.management.base import BaseCommand
from news.models import Post, Category


class Command(BaseCommand):  # D14.4
    help = 'Подсказка вашей команды'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no>>>:')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))

        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(categories=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Успешно удалены все новости из категории  {category.name}'))

        except Category.DoesNotExist:  # в случае неправильного подтверждения говорим, что в доступе отказано
            self.stdout.write(self.style.ERROR(f'Не удалось найти категорию  {options["category"]}'))