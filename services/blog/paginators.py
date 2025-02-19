from rest_framework.pagination import CursorPagination, LimitOffsetPagination, PageNumberPagination


class PageNumberPaginationForPosts(PageNumberPagination):
    """Пагинация списка постов для постраничного отображения"""

    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 50


class CursorPaginationForPostsInCategoryList(CursorPagination):
    """Пагинация для списка постов в разделе "Категории" с помощью курсора"""

    page_size = 10
    ordering = ('-publish', '-id')


class LimitOffsetPaginationForVideoList(LimitOffsetPagination):
    """Пагинация для списка видеозаписей на основе смещения и лимита"""

    default_limit = 3
    max_limit = 50


def get_paginator_for_post_list(
    type_pagination: str | None = None,
) -> PageNumberPagination | CursorPaginationForPostsInCategoryList:
    """
    Возвращает экземпляр пагинации для списка постов в зависимости от типа пагинации.
    Если передан 'cursor', возвращается курсорная пагинация, по умолчанию — постраничная.
    """
    if type_pagination == 'cursor':
        return CursorPaginationForPostsInCategoryList()
    return PageNumberPaginationForPosts()
