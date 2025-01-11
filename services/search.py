import datetime

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import QuerySet

from blog_by_me_DRF.settings import LANGUAGES


def search_by_tag(object_list: QuerySet, tag_slug: str) -> QuerySet:
    """Функция фильтрует записи по тегу"""
    return object_list.filter(tags__slug=tag_slug)


def search_by_date(object_list: QuerySet, date: str) -> QuerySet:
    """Функция фильтрует записи по дате"""
    format_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    return object_list.filter(created__date=format_date)


def search_by_q(q: str, object_list: QuerySet, current_language: str) -> QuerySet:
    """
    Поиск по названию и содержанию в зависимости от выбранного языка,
    сортировка результатов поиска с использованием специальных классов для PostgeSQL
    """
    if current_language == LANGUAGES[0][0]:  # наличие русского языка в запросе
        search_vector = SearchVector('title_ru', 'body_ru')
    else:
        search_vector = SearchVector('title_en', 'body_en')

    search_query = SearchQuery(q)

    post_list = (
        object_list.annotate(search=search_vector, rank=SearchRank(search_vector, search_query))
        .filter(search=search_query)
        .order_by('-rank')
    )
    return post_list
