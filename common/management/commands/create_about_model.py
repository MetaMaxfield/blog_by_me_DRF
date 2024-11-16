import logging

from django.core.management import BaseCommand

from company.models import About

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Создает экземпляр модели About для хранения информации о компании.'

    def handle(self, *args, **options):
        if About.objects.exists():
            info = 'Экземпляр модели About с информацией о компании уже существует.'
            logger.error(info)
            self.stdout.write(self.style.ERROR(info))
        else:
            info = 'Экземпляр модели About с информацией о компании создан.'
            About.objects.create()
            self.stdout.write(self.style.SUCCESS(info))
