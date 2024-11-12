import logging

from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from blog_by_me_DRF.settings import TITLE_AUTHOR_GROUP, TITLE_MODERATOR_GROUP

logger = logging.getLogger(__name__)

GROUPS = {
    TITLE_AUTHOR_GROUP: {
        'Категория': ['add', 'change', 'view'],
        'Комментарий': [
            'view',
        ],
        'Пост': ['add', 'delete', 'change', 'view'],
        'Рейтинг': [
            'view',
        ],
        'Видеозапись': ['add', 'delete', 'change', 'view'],
        'user': [
            'change',
        ],
        'Запрос от пользователя блога': [
            'view',
        ],
        'tag': ['add', 'view'],
        'tagged item': ['add', 'view'],
    },
    TITLE_MODERATOR_GROUP: {
        'Категория': ['add', 'delete', 'change', 'view'],
        'Комментарий': ['add', 'delete', 'change', 'view'],
        'Пост': ['add', 'delete', 'change', 'view'],
        'Рейтинг': [
            'view',
        ],
        'Видеозапись': ['add', 'delete', 'change', 'view'],
        'Запрос от пользователя блога': ['view', 'delete'],
        'Содержание страницы "О нас"': ['add', 'delete', 'change', 'view'],
        'user': [
            'view',
        ],
        'tag': ['add', 'delete', 'change', 'view'],
        'tagged item': ['add', 'delete', 'change', 'view'],
    },
}


class Command(BaseCommand):
    help = "Создает группы с разрешениями для пользователей"

    def handle(self, *args, **options):

        # Цикл групп в списке
        for group_name in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group_name)

            # Сообщение о производимом действии
            if created:
                self.stdout.write(f'\nСоздание группы {group_name}.')
            else:
                self.stdout.write(f'\nГруппа {group_name} уже существует, права будут обновлены.')

            # Цикл моделей в группах
            for app_model in GROUPS[group_name]:

                # Цикл разрешений в моделях групп
                for permission_name in GROUPS[group_name][app_model]:

                    # Создание названия разрешения Django.
                    name = f"Can {permission_name} {app_model}"
                    self.stdout.write(f'\tСоздание разрешения {name}...')

                    # Проверка существования разрешения для добавления в группу
                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logger.warning(f'Разрешение с именем "{name}" не найдено.')
                        self.stdout.write(self.style.WARNING(f'\tРазрешение с именем "{name}" не найдено.'))
                        continue

                    # Добавление разрешения к группе
                    new_group.permissions.add(model_add_perm)
                    self.stdout.write('\tРазрешение добавлено к группе.')
