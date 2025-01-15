import datetime

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import QuerySet
from django.utils.translation import gettext as _

from blog_by_me_DRF.settings import LANGUAGES
from services.exceptions import NoContent


def search_by_tag(object_list: QuerySet, tag_slug: str) -> QuerySet:
    """Функция фильтрует записи по тегу"""

    post_list = object_list.filter(tags__slug=tag_slug)

    if not post_list.exists():
        raise NoContent(_('Посты с заданным тегом не найдены'))
    return post_list


def search_by_date(object_list: QuerySet, date: str) -> QuerySet:
    """Функция фильтрует записи по дате"""

    format_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    post_list = object_list.filter(created__date=format_date)

    if not post_list.exists():
        raise NoContent(_('Посты с датой "{date}" не найдены').format(date=date))
    return post_list


def search_by_q(q: str, object_list: QuerySet, current_language: str) -> QuerySet:
    """
    Поиск по названию и содержанию в зависимости от выбранного языка,
    сортировка результатов поиска с использованием специальных классов для PostgreSQL
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

    if not post_list.exists():
        raise NoContent(_('Посты по запросу "{q}" не найдены').format(q=q))
    return post_list
