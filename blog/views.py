from django.utils.translation import gettext as _
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from blog import serializers
from blog_by_me_DRF import settings
from services import caching, rating, search
from services.blog import paginators, validators
from services.client_ip import get_client_ip
from services.rating import ServiceUserRating

# class PostsView(APIView):
#     """Вывод постов блога"""
#
#     def get(self, request: Request) -> Response:
#         object_list = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)
#         paginator = paginators.PageNumberPaginationForPosts()
#         paginated_object_list = paginator.paginate_queryset(object_list, request)
#         serializer = serializers.PostsSerializer(paginated_object_list, many=True)
#         return paginator.get_paginated_response(serializer.data)


class PostsView(generics.ListAPIView):
    """Вывод постов блога"""

    serializer_class = serializers.PostsSerializer
    pagination_class = paginators.PageNumberPaginationForPosts

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
#         paginator = paginators.PageNumberPaginationForPosts()
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
#         paginator = paginators.PageNumberPaginationForPosts()
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
#         paginator = paginators.PageNumberPaginationForPosts()
#         paginated_post_list = paginator.paginate_queryset(post_list, request)
#
#         serializer = serializers.PostsSerializer(paginated_post_list, many=True)
#         return paginator.get_paginated_response(serializer.data)


class FilterTagPostsView(PostsView):
    """Вывод постов с фильтрацией по тегу"""

    def filter_queryset(self, queryset):
        return search.search_by_tag(queryset, self.kwargs['tag_slug'])


class AddCommentView(APIView):
    """Добавление комментария к посту"""

    def post(self, request: Request) -> Response:
        comment = serializers.AddCommentSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
            return Response({'message': _('Комментарий успешно добавлен.')}, status=status.HTTP_201_CREATED)
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """Вывод отдельного поста"""

    def get(self, request: Request, slug: str) -> Response:
        post = caching.get_cached_objects_or_queryset(settings.KEY_POST_DETAIL, slug=slug)
        post.user_rating = rating.has_user_rated_post(get_client_ip(request), post)
        serializer = serializers.PostDetailSerializer(post)
        return Response(serializer.data)


class CategoryListView(APIView):
    """Вывод списка категорий и постов к ним"""

    def get(self, request: Request) -> Response:
        category_list = caching.get_cached_objects_or_queryset(settings.KEY_CATEGORIES_LIST)
        post_list = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)

        paginator = paginators.CursorPaginationForPostsInCategoryList()
        paginated_post_list = paginator.paginate_queryset(post_list, request)

        category_serializer = serializers.CategoryListSerializer(category_list, many=True)
        posts_serializer = serializers.PostsSerializer(paginated_post_list, many=True)
        return paginator.get_paginated_response(
            {
                'category_list': category_serializer.data,
                'post_list': posts_serializer.data,
            }
        )


class VideoListView(APIView):
    """Вывод всех видеозаписей"""

    def get(self, request: Request) -> Response:
        video_list = caching.get_cached_objects_or_queryset(settings.KEY_VIDEOS_LIST)
        paginator = paginators.LimitOffsetPaginationForVideoList()
        paginated_video_list = paginator.paginate_queryset(video_list, request)
        videos_serializer = serializers.VideoListSerializer(paginated_video_list, many=True)
        return paginator.get_paginated_response(videos_serializer.data)


class AddRatingView(APIView):
    """Добавление рейтинга к посту"""

    def put(self, request: Request) -> Response:
        # Получаем IP пользователя
        ip = get_client_ip(request)

        # Создаём объект класса для работы с рейтингом
        service_rating = ServiceUserRating(ip, post_id=request.data['post'], mark_id=request.data['mark'])

        # Получаем текущий рейтинг пользователя для указанного IP-адреса и поста,
        # если он существует в базе данных. В противном случае возвращает None
        existing_rating = service_rating.existing_rating

        # Сериализуем рейтинг для добавления/обновления
        rating_serializer = serializers.AddRatingSerializer(instance=existing_rating, data=request.data)

        if rating_serializer.is_valid():

            # Обновляем рейтинг пользователя на основе выбранной оценки
            # и получаем соответствующее сообщение и статусный код для совершённого действия
            message, status_code = service_rating.update_author_rating_with_return_message_and_status_code()

            rating_serializer.save(ip=ip)

            return Response({'message': _(message)}, status=status_code)

        return Response(rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
