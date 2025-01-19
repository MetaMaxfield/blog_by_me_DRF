from django.utils.translation import gettext as _
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from blog import serializers
from blog_by_me_DRF import settings
from services import caching, search
from services.blog import paginators, validators
from services.client_ip import get_client_ip
from services.rating import ServiceUserRating

# class PostsView(APIView):
#     """Вывод постов блога"""
#
#     def get(self, request: Request) -> Response:
#         object_list = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)
#         paginator = paginators.get_paginator_for_post_list(request.query_params.get('pagination'))
#         paginated_object_list = paginator.paginate_queryset(object_list, request)
#         serializer = serializers.PostsSerializer(paginated_object_list, many=True)
#         return paginator.get_paginated_response(serializer.data)


class PostsView(generics.ListAPIView):
    """Вывод постов блога"""

    serializer_class = serializers.PostsSerializer

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            self._paginator = paginators.get_paginator_for_post_list(self.request.query_params.get('pagination'))
        return self._paginator

    def get_queryset(self):
        return caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)


# class SearchPostView(APIView):
#     """Вывод результатов поиска постов блога"""
#
#     def get(self, request: Request) -> Response:
#         q = request.query_params.get('q')
#         validators.validate_q_param(q)
#
#         post_list = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)
#         post_list = search.search_by_q(q, post_list, request.LANGUAGE_CODE)
#
#         paginator = paginators.get_paginator_for_post_list(request.query_params.get('pagination'))
#         paginated_post_list = paginator.paginate_queryset(post_list, request)
#         serializer = serializers.PostsSerializer(paginated_post_list, many=True)
#         return paginator.get_paginated_response(serializer.data)


class SearchPostView(PostsView):
    """Вывод результатов поиска постов блога"""

    def get(self, request, *args, **kwargs):
        self.kwargs['q'] = self.request.query_params.get('q')
        validators.validate_q_param(self.kwargs['q'])
        return super().get(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        return search.search_by_q(self.kwargs['q'], queryset, self.request.LANGUAGE_CODE)


# class FilterDatePostsView(APIView):
#     """Вывод постов с фильтрацией по дате"""
#
#     def get(self, request: Request, date_post: str) -> Response:
#         validators.validate_date_format(date_post)
#
#         post_list = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)
#         post_list = search.search_by_date(post_list, date_post)
#
#         paginator = paginators.get_paginator_for_post_list(request.query_params.get('pagination'))
#         paginated_post_list = paginator.paginate_queryset(post_list, request)
#
#         serializer = serializers.PostsSerializer(paginated_post_list, many=True)
#         return paginator.get_paginated_response(serializer.data)


class FilterDatePostsView(PostsView):
    """Вывод постов с фильтрацией по дате"""

    def get(self, request, *args, **kwargs):
        validators.validate_date_format(self.kwargs['date_post'])
        return super().get(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        return search.search_by_date(queryset, self.kwargs['date_post'])


# class FilterTagPostsView(APIView):
#     """Вывод постов с фильтрацией по тегу"""
#
#     def get(self, request: Request, tag_slug: str) -> Response:
#         post_list = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)
#         post_list = search.search_by_tag(post_list, tag_slug)
#
#         paginator = paginators.get_paginator_for_post_list(request.query_params.get('pagination'))
#         paginated_post_list = paginator.paginate_queryset(post_list, request)
#
#         serializer = serializers.PostsSerializer(paginated_post_list, many=True)
#         return paginator.get_paginated_response(serializer.data)


class FilterTagPostsView(PostsView):
    """Вывод постов с фильтрацией по тегу"""

    def filter_queryset(self, queryset):
        return search.search_by_tag(queryset, self.kwargs['tag_slug'])


# class AddCommentView(APIView):
#     """Добавление комментария к посту"""
#
#     def post(self, request: Request) -> Response:
#         comment = serializers.AddCommentSerializer(data=request.data)
#         if comment.is_valid():
#             comment.save()
#             return Response({'message': _('Комментарий успешно добавлен.')}, status=status.HTTP_201_CREATED)
#         return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommentView(generics.CreateAPIView):
    """Добавление комментария к посту"""

    serializer_class = serializers.AddCommentSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'message': _('Комментарий успешно добавлен.')}, status=status.HTTP_201_CREATED)


# class PostDetailView(APIView):
#     """Вывод отдельного поста"""
#
#     def get(self, request: Request, slug: str) -> Response:
#         post = caching.get_cached_objects_or_queryset(settings.KEY_POST_DETAIL, slug=slug)
#         serializer = serializers.PostDetailSerializer(post, context={'request': request})
#         return Response(serializer.data)


class PostDetailView(generics.RetrieveAPIView):
    """Вывод отдельного поста"""

    serializer_class = serializers.PostDetailSerializer

    def get_object(self):
        return caching.get_cached_objects_or_queryset(settings.KEY_POST_DETAIL, slug=self.kwargs['slug'])


# class CategoryListView(APIView):
#     """Вывод списка категорий и постов к ним"""
#
#     def get(self, request: Request) -> Response:
#         category_list = caching.get_cached_objects_or_queryset(settings.KEY_CATEGORIES_LIST)
#         serializer = serializers.CategoryListSerializer(category_list, many=True)
#         return Response(serializer.data)


class CategoryListView(generics.ListAPIView):
    """Вывод списка категорий и постов к ним"""

    serializer_class = serializers.CategoryListSerializer

    def get_queryset(self):
        return caching.get_cached_objects_or_queryset(settings.KEY_CATEGORIES_LIST)


# class VideoListView(APIView):
#     """Вывод всех видеозаписей"""
#
#     def get(self, request: Request) -> Response:
#         video_list = caching.get_cached_objects_or_queryset(settings.KEY_VIDEOS_LIST)
#         paginator = paginators.LimitOffsetPaginationForVideoList()
#         paginated_video_list = paginator.paginate_queryset(video_list, request)
#         videos_serializer = serializers.VideoListSerializer(paginated_video_list, many=True)
#         return paginator.get_paginated_response(videos_serializer.data)


class VideoListView(generics.ListAPIView):
    """Вывод всех видеозаписей"""

    serializer_class = serializers.VideoListSerializer
    pagination_class = paginators.LimitOffsetPaginationForVideoList

    def get_queryset(self):
        return caching.get_cached_objects_or_queryset(settings.KEY_VIDEOS_LIST)


# class AddRatingView(APIView):
#     """
#     Добавление рейтинга к посту.
#
#     ВНИМАНИЕ: Данное представление реализует PUT as create.
#     Если объект не найден, он будет автоматически создан при выполнении PUT-запроса.
#     """
#
#     def put(self, request: Request) -> Response:
#         # Получаем IP пользователя
#         ip = get_client_ip(request)
#
#         # Создаём объект класса для работы с рейтингом
#         service_rating = ServiceUserRating(ip, post_id=request.data['post'], mark_id=request.data['mark'])
#
#         # Получаем текущий рейтинг пользователя для указанного IP-адреса и поста,
#         # если он существует в базе данных. В противном случае возвращает None
#         existing_rating = service_rating.existing_rating
#
#         # Сериализуем рейтинг для добавления/обновления
#         rating_serializer = serializers.AddRatingSerializer(instance=existing_rating, data=request.data)
#
#         if rating_serializer.is_valid():
#
#             # Обновляем рейтинг пользователя на основе выбранной оценки
#             # и получаем соответствующее сообщение и статусный код для совершённого действия
#             message, status_code = service_rating.update_author_rating_with_return_message_and_status_code()
#
#             rating_serializer.save(ip=ip)
#
#             return Response({'message': _(message)}, status=status_code)
#
#         return Response(rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddRatingView(generics.UpdateAPIView):
    """
    Добавление рейтинга к посту.

    ВНИМАНИЕ: Данное представление реализует PUT as create.
    Если объект не найден, он будет автоматически создан при выполнении PUT-запроса.
    """

    serializer_class = serializers.AddRatingSerializer

    def get_object(self):
        # Получаем текущий рейтинг пользователя для указанного IP-адреса и поста,
        # если он существует в базе данных. В противном случае возвращает None
        return self.service_rating.existing_rating

    def perform_update(self, serializer):
        # Обновляем рейтинг пользователя на основе выбранной оценки
        # и получаем соответствующее сообщение и статусный код для совершённого действия
        self.message, self.status_code = self.service_rating.update_author_rating_with_return_message_and_status_code()

        serializer.save(ip=self.kwargs['ip'])

    def update(self, request, *args, **kwargs):
        # Получаем IP пользователя
        self.kwargs['ip'] = get_client_ip(request)

        # Создаём объект класса для работы с рейтингом
        self.service_rating = ServiceUserRating(
            self.kwargs['ip'], post_id=request.data['post'], mark_id=request.data['mark']
        )

        super().update(request, *args, **kwargs)
        return Response({'message': _(self.message)}, status=self.status_code)


class TopPostsView(APIView):
    """Вывод трёх постов с наивысшим рейтингом"""

    def get(self, request: Request) -> Response:
        top_posts = caching.get_cached_objects_or_queryset(settings.KEY_TOP_POSTS)
        serializer = serializers.PostsSerializer(top_posts, many=True, fields=('title', 'body', 'url'))
        return Response(serializer.data)


class LastPostsView(APIView):
    """Вывод трех последних опубликованных постов"""

    def get(self, request: Request) -> Response:
        last_posts = caching.get_cached_objects_or_queryset(settings.KEY_LAST_POSTS)
        serializer = serializers.PostsSerializer(last_posts, many=True, fields=('image', 'title', 'body', 'url'))
        return Response(serializer.data)


class DaysInCalendarView(APIView):
    """Вывод дат публикации постов для заданного месяца"""

    def get(self, request: Request, year: int, month: int) -> Response:
        days_with_post = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_CALENDAR, year=year, month=month)
        return Response(days_with_post)


class TopTagsView(APIView):
    """Вывод десяти самых популярных тегов и количества постов к ним"""

    def get(self, request: Request) -> Response:
        tags = caching.get_cached_objects_or_queryset(settings.KEY_ALL_TAGS)
        serializer = serializers.TopTagsSerializer(tags, many=True)
        return Response(serializer.data)
