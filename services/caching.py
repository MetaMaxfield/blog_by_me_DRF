from typing import Dict, Union

from django.core.cache import cache
from django.db.models import QuerySet

from blog_by_me_DRF import settings
from services.queryset import qs_definition


def _get_cache_time(qs_key: str) -> int:
    """Получение времени кэширования в зависимости от типа данных"""
    return settings.CACHE_TIMES.get(qs_key, 300)


def get_cached_objects_or_queryset(
    qs_key: str, **kwargs: Dict[str, Union[str, int]]
) -> QuerySet | settings.ObjectModel:
    """
    Получения кэша или вызов QS

    Порядок формирования ключа-инициализатора init_key для кэша:
    1. Если ключ запроса - KEY_POSTS_CALENDAR, используем год и месяц (формат "год/месяц");
    2. Если передан 'slug', он используется как доп. ключ для данных отдельного поста
       (передаётся только вместе с ключом KEY_POST_DETAIL);
    3. Если передан 'pk', он используется как доп. ключ для данных автора
       (передаётся только вместе с ключом KEY_AUTHOR_DETAIL);
    4. Если ключ запроса не KEY_POSTS_CALENDAR, а 'slug' и 'pk' не переданы, ключ остаётся пустой строкой
       (отсутствие этих условий подразумевает необходимость в получении общих данных, по типу списков объекта модели).
    """

    # Формируем init_key для кэша
    if qs_key == settings.KEY_POSTS_CALENDAR:
        init_key = f'{kwargs["year"]}/{kwargs["month"]}'
    else:
        init_key = kwargs.get('slug') or kwargs.get('pk') or ''

    # Проверяем наличие данных в кэше
    object_list_or_object = cache.get(f'{settings.CACHE_KEY}{qs_key}{init_key}')

    if not object_list_or_object:

        # Генерируем данные, если их нет в кэше
        object_list_or_object = qs_definition(qs_key, **kwargs)

        # Получаем время кэширования
        cache_time = _get_cache_time(qs_key)

        # Сохраняем данные в кэше
        cache.set(f'{settings.CACHE_KEY}{qs_key}{init_key}', object_list_or_object, cache_time)

    return object_list_or_object
