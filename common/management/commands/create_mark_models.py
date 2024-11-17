import logging

from django.core.management import BaseCommand

from blog.models import Mark
from blog_by_me_DRF.settings import TITLE_DISLIKE_MARK, TITLE_LIKE_MARK

logger = logging.getLogger(__name__)

MARKS_LIST = [
    {'id': 1, 'nomination': TITLE_LIKE_MARK, 'value': 1},
    {'id': 2, 'nomination': TITLE_DISLIKE_MARK, 'value': -1},
]


class Command(BaseCommand):

    help = 'Создает экземпляры модели Mark для возможности оценивания постов.'

    def handle(self, *args, **options):

        # Цикл создания объектов модели Mark
        for mark in MARKS_LIST:

            self.stdout.write(f'\nСоздание оценки {mark["nomination"]}...')

            # Создание или обновление существующей оценки
            new_mark, created = Mark.objects.update_or_create(
                id=mark['id'], nomination=mark['nomination'], value=mark['value']
            )

            # Оповещение при создании объекта модели
            if created:
                info = f'Оценка с наименованием "{mark["nomination"]}" создана.'
                self.stdout.write(self.style.SUCCESS(info))

            # Оповещение при обновлении объекта модели
            else:
                info = (
                    f'Оценка с наименованием "{mark["nomination"]}" уже существует. '
                    f'Данные экземпляра модели обновлены.'
                )
                logger.warning(info)
                self.stdout.write(self.style.WARNING(info))
