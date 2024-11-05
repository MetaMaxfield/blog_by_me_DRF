from django.core.management import BaseCommand

from company.models import About


class Command(BaseCommand):
    help = 'Создает экземпляр модели About для хранения информации о компании.'

    def handle(self, *args, **options):
        if About.objects.exists():
            self.stdout.write(self.style.ERROR('Экземпляр модели About с информацией о компании уже существует.'))
        else:
            About.objects.create()
            self.stdout.write(self.style.SUCCESS('Экземпляр модели About с информацией о компании создан.'))
