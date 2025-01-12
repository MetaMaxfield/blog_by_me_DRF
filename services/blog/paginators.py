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
