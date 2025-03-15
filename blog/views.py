from django.utils.translation import gettext as _
from rest_framework import mixins, status, viewsets  # , generics
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from blog import serializers
from blog_by_me_DRF import settings
from services import caching, queryset, search
from services.blog import paginators, validators
from services.client_ip import get_client_ip
from services.rating import ServiceUserRating
from services.renderer import NoHTMLFormBrowsableAPIRenderer

# class PostsView(APIView):
#     """Вывод постов блога"""
#
#     def get(self, request: Request) -> Response:
#         object_list = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)
#         paginator = paginators.get_paginator_for_post_list(request.query_params.get('pagination'))
#         paginated_object_list = paginator.paginate_queryset(object_list, request)
#         serializer = serializers.PostsSerializer(paginated_object_list, many=True)
#         return paginator.get_paginated_response(serializer.data)


# class PostsView(generics.ListAPIView):
#     """Вывод постов блога"""
#
#     serializer_class = serializers.PostsSerializer
#
#     @property
#     def paginator(self):
#         if not hasattr(self, '_paginator'):
#             self._paginator = paginators.get_paginator_for_post_list(self.request.query_params.get('pagination'))
#         return self._paginator
#
#     def get_queryset(self):
#         return caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)


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


# class SearchPostView(PostsView):
#     """Вывод результатов поиска постов блога"""
#
#     def list(self, request, *args, **kwargs):
#         self.kwargs['q'] = self.request.query_params.get('q')
#         validators.validate_q_param(self.kwargs['q'])
#         return super().list(request, *args, **kwargs)
#
#     def filter_queryset(self, queryset):
#         return search.search_by_q(self.kwargs['q'], queryset, self.request.LANGUAGE_CODE)


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


# class FilterDatePostsView(PostsView):
#     """Вывод постов с фильтрацией по дате"""
#
#     def list(self, request, *args, **kwargs):
#         validators.validate_date_format(self.kwargs['date_post'])
#         return super().list(request, *args, **kwargs)
#
#     def filter_queryset(self, queryset):
#         return search.search_by_date(queryset, self.kwargs['date_post'])


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


# class FilterTagPostsView(PostsView):
#     """Вывод постов с фильтрацией по тегу"""
#
#     def filter_queryset(self, queryset):
#         return search.search_by_tag(queryset, self.kwargs['tag_slug'])


# class PostDetailView(APIView):
#     """Вывод отдельного поста"""
#
#     def get(self, request: Request, slug: str) -> Response:
#         post = caching.get_cached_objects_or_queryset(settings.KEY_POST_DETAIL, slug=slug)
#         serializer = serializers.PostDetailSerializer(post, context={'request': request})
#         return Response(serializer.data)


# class PostDetailView(generics.RetrieveAPIView):
#     """Вывод отдельного поста"""
#
#     serializer_class = serializers.PostDetailSerializer
#
#     def get_object(self):
#         return caching.get_cached_objects_or_queryset(settings.KEY_POST_DETAIL, slug=self.kwargs['slug'])


# class TopPostsView(APIView):
#     """Вывод трёх постов с наивысшим рейтингом"""
#
#     def get(self, request: Request) -> Response:
#         top_posts = caching.get_cached_objects_or_queryset(settings.KEY_TOP_POSTS)
#         serializer = serializers.PostsSerializer(top_posts, many=True, fields=('title', 'body', 'url'))
#         return Response(serializer.data)


# class TopPostsView(generics.ListAPIView):
#     """Вывод трёх постов с наивысшим рейтингом"""
#
#     serializer_class = serializers.PostsSerializer
#
#     def get_queryset(self):
#         return caching.get_cached_objects_or_queryset(settings.KEY_TOP_POSTS)
#
#     def get_serializer(self, *args, **kwargs):
#         # Добавление 'fields' для выбора сериализуемых полей (динамический выбор полей для сериализации)
#         kwargs['fields'] = ('title', 'body', 'url')
#         return super().get_serializer(*args, **kwargs)


# class LastPostsView(APIView):
#     """Вывод трех последних опубликованных постов"""
#
#     def get(self, request: Request) -> Response:
#         last_posts = caching.get_cached_objects_or_queryset(settings.KEY_LAST_POSTS)
#         serializer = serializers.PostsSerializer(last_posts, many=True, fields=('image', 'title', 'body', 'url'))
#         return Response(serializer.data)


# class LastPostsView(generics.ListAPIView):
#     """Вывод трех последних опубликованных постов"""
#
#     serializer_class = serializers.PostsSerializer
#
#     def get_queryset(self):
#         return caching.get_cached_objects_or_queryset(settings.KEY_LAST_POSTS)
#
#     def get_serializer(self, *args, **kwargs):
#         # Добавление 'fields' для выбора сериализуемых полей (динамический выбор полей для сериализации)
#         kwargs['fields'] = ('image', 'title', 'body', 'url')
#         return super().get_serializer(*args, **kwargs)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для работы с постами блога.

    Поддерживаемые действия:
    - Вывод списка постов
    - Поиск постов по запросу
    - Фильтрация постов по дате
    - Фильтрация постов по тегу
    - Вывод отдельного поста
    - Вывод трёх постов с наивысшим рейтингом
    - Вывод трёх последних опубликованных постов
    """

    lookup_field = 'url'
    lookup_url_kwarg = 'slug'

    @action(detail=False)
    def search(self, request, *args, **kwargs):
        self.kwargs['q'] = self.request.query_params.get('q')
        validators.validate_q_param(self.kwargs['q'])
        return self.list(request, *args, **kwargs)

    @action(detail=False, url_path=r'date/(?P<date_post>[^/]+)')
    def filter_by_date(self, request, *args, **kwargs):
        validators.validate_date_format(self.kwargs['date_post'])
        return self.list(request, *args, **kwargs)

    @action(detail=False, url_path=r'tag/(?P<tag_slug>[^/]+)')
    def filter_by_tag(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=False, url_path=r'top-posts')
    def top_posts(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=False, url_path=r'last-posts')
    def last_posts(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        if self.action == 'top_posts':
            return caching.get_cached_objects_or_queryset(settings.KEY_TOP_POSTS)
        elif self.action == 'last_posts':
            return caching.get_cached_objects_or_queryset(settings.KEY_LAST_POSTS)
        else:
            return caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)

    def filter_queryset(self, queryset):
        if self.action == 'search':
            return search.search_by_q(self.kwargs['q'], queryset, self.request.LANGUAGE_CODE)
        elif self.action == 'filter_by_date':
            return search.search_by_date(queryset, self.kwargs['date_post'])
        elif self.action == 'filter_by_tag':
            return search.search_by_tag(queryset, self.kwargs['tag_slug'])
        else:
            return queryset

    def get_object(self):
        return caching.get_cached_objects_or_queryset(settings.KEY_POST_DETAIL, slug=self.kwargs['slug'])

    @property
    def paginator(self):
        # Динамический выбор пагинации через параметр 'pagination'
        if not hasattr(self, '_paginator'):
            self._paginator = paginators.get_paginator_for_post_list(self.request.query_params.get('pagination'))
        return self._paginator

    def get_serializer(self, *args, **kwargs):
        # Добавление 'fields' для выбора сериализуемых полей (динамический выбор полей для сериализации)
        if self.action == 'top_posts':
            kwargs['fields'] = ('title', 'body', 'url')
        elif self.action == 'last_posts':
            kwargs['fields'] = ('image', 'title', 'body', 'url')
        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.detail:
            return serializers.PostDetailSerializer
        return serializers.PostsSerializer


# class CategoryListView(APIView):
#     """Вывод списка категорий"""
#
#     def get(self, request: Request) -> Response:
#         category_list = caching.get_cached_objects_or_queryset(settings.KEY_CATEGORIES_LIST)
#         serializer = serializers.CategoryListSerializer(category_list, many=True)
#         return Response(serializer.data)


# class CategoryListView(generics.ListAPIView):
#     """Вывод списка категорий"""
#
#     serializer_class = serializers.CategoryListSerializer
#
#     def get_queryset(self):
#         return caching.get_cached_objects_or_queryset(settings.KEY_CATEGORIES_LIST)


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вывод списка категорий"""

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


# class VideoListView(generics.ListAPIView):
#     """Вывод всех видеозаписей"""
#
#     serializer_class = serializers.VideoListSerializer
#     pagination_class = paginators.LimitOffsetPaginationForVideoList
#
#     def get_queryset(self):
#         return caching.get_cached_objects_or_queryset(settings.KEY_VIDEOS_LIST)


class VideoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вывод всех видеозаписей"""

    serializer_class = serializers.VideoListSerializer
    pagination_class = paginators.LimitOffsetPaginationForVideoList

    def get_queryset(self):
        return caching.get_cached_objects_or_queryset(settings.KEY_VIDEOS_LIST)


# class GetAddRatingView(APIView):
#     """
#     Вывод и создание/обновление рейтинга пользователя к посту.
#
#     ВНИМАНИЕ: Представление реализует UPSERT подход.
#     Если объект не найден, он будет автоматически создан при выполнении POST-запроса.
#     """
#
#     def setup_rating_service(self, request: Request, slug: str):
#         """Получение ip пользователя и создание объекта класса для работы с рейтингом"""
#         self.ip = get_client_ip(request)
#         self.service_rating = ServiceUserRating(
#             ip=self.kwargs['ip'],
#             post_slug=kwargs['slug'],
#             mark_id=request.data.get('mark'),
#             http_method=request.method
#         )
#
#     def get(self, request: Request, slug: str) -> Response:
#         self.setup_rating_service(request, slug)
#         rating = self.service_rating.existing_rating
#         rating_serializer = serializers.RatingDetailSerializer(rating)
#         return Response(rating_serializer.data)
#
#     def post(self, request: Request, slug: str) -> Response:
#         self.setup_rating_service(request, slug)
#
#         # Получаем текущий рейтинг пользователя для указанного IP-адреса и поста,
#         # если он существует в базе данных. В противном случае возвращает None
#         rating = self.service_rating.existing_rating
#
#         rating_serializer = serializers.AddRatingSerializer(rating, data=request.data, context={'slug': slug})
#
#         if rating_serializer.is_valid():
#             # Обновляем рейтинг пользователя на основе выбранной оценки
#             # и получаем соответствующее сообщение и статусный код для совершённого действия
#             message, status_code = self.service_rating.update_author_rating_with_return_message_and_status_code()
#
#             rating_serializer.save(ip=self.ip)
#             return Response({'message': _(message)}, status=status_code)
#
#         return Response(rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class GetAddRatingView(generics.RetrieveAPIView, mixins.UpdateModelMixin):
#     """
#     Вывод и создание/обновление рейтинга пользователя к посту.
#
#     ВНИМАНИЕ: Представление реализует UPSERT подход.
#     Если объект не найден, он будет автоматически создан при выполнении POST-запроса.
#     """
#
#     renderer_classes = [JSONRenderer, NoHTMLFormBrowsableAPIRenderer]
#
#     def setup_rating_service(self, request, *args, **kwargs):
#         """Получение ip пользователя и создание объекта класса для работы с рейтингом"""
#         self.kwargs['ip'] = get_client_ip(request)
#         self.service_rating = ServiceUserRating(
#             ip=self.kwargs['ip'],
#             post_slug=kwargs['slug'],
#             mark_id=request.data.get('mark'),
#             http_method=request.method
#         )
#
#     def retrieve(self, request, *args, **kwargs):
#         self.setup_rating_service(request, *args, **kwargs)
#         return super().retrieve(self, request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         self.setup_rating_service(request, *args, **kwargs)
#         self.update(request, *args, **kwargs)
#         return Response({'message': _(self.message)}, status=self.status_code)
#
#     def get_object(self):
#         # Получаем текущий рейтинг пользователя для указанного IP-адреса и поста,
#         # если он существует в базе данных. В противном случае возвращает None
#         return self.service_rating.existing_rating
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return serializers.RatingDetailSerializer
#         elif self.request.method == 'POST':
#             return serializers.AddRatingSerializer
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['slug'] = self.kwargs['slug']
#         return context
#
#     def perform_update(self, serializer):
#         # Обновляем рейтинг автора на основе выбранной оценки
#         # и получаем соответствующее сообщение и статусный код для совершённого действия
#         self.message, self.status_code = \
#             self.service_rating.update_author_rating_with_return_message_and_status_code()
#
#         serializer.save(ip=self.kwargs['ip'])


class RatingViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Вьюсет для работы с рейтингом пользователя к посту.

    Поддерживаемые действия:
    - Вывод существующего рейтинга
    - Создание/обновление рейтинга

    ВНИМАНИЕ: Представление реализует UPSERT подход.
    Если объект не найден, он будет автоматически создан при выполнении POST-запроса.
    """

    renderer_classes = [JSONRenderer, NoHTMLFormBrowsableAPIRenderer]

    def setup_rating_service(self, request, *args, **kwargs):
        """Получение ip пользователя и создание объекта класса для работы с рейтингом"""
        self.kwargs['ip'] = get_client_ip(request)
        self.service_rating = ServiceUserRating(
            ip=self.kwargs['ip'], post_slug=kwargs['slug'], mark_id=request.data.get('mark'), http_method=request.method
        )

    def retrieve(self, request, *args, **kwargs):
        self.setup_rating_service(request, *args, **kwargs)
        return super().retrieve(request, *args, **kwargs)

    def create_or_update(self, request, *args, **kwargs):
        self.setup_rating_service(request, *args, **kwargs)
        super().update(request, *args, **kwargs)
        return Response({'message': _(self.message)}, status=self.status_code)

    def get_object(self):
        # Получаем текущий рейтинг пользователя для указанного IP-адреса и поста,
        # если он существует в базе данных. В противном случае возвращает None
        return self.service_rating.existing_rating

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.RatingDetailSerializer
        elif self.action == 'create_or_update':
            return serializers.AddRatingSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['slug'] = self.kwargs['slug']
        return context

    def perform_update(self, serializer):
        # Обновляем рейтинг пользователя на основе выбранной оценки
        # и получаем соответствующее сообщение и статусный код для совершённого действия
        self.message, self.status_code = self.service_rating.update_author_rating_with_return_message_and_status_code()

        serializer.save(ip=self.kwargs['ip'])


class DaysInCalendarView(APIView):
    """Вывод дат публикации постов для заданного месяца"""

    def get(self, request: Request, year: int, month: int) -> Response:
        days_with_post = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_CALENDAR, year=year, month=month)
        return Response(days_with_post)


# class TopTagsView(APIView):
#     """Вывод десяти самых популярных тегов и количества постов к ним"""
#
#     def get(self, request: Request) -> Response:
#         tags = caching.get_cached_objects_or_queryset(settings.KEY_ALL_TAGS)
#         serializer = serializers.TopTagsSerializer(tags, many=True)
#         return Response(serializer.data)


# class TopTagsView(generics.ListAPIView):
#     """Вывод десяти самых популярных тегов и количества постов к ним"""
#
#     serializer_class = serializers.TopTagsSerializer
#
#     def get_queryset(self):
#         return caching.get_cached_objects_or_queryset(settings.KEY_ALL_TAGS)


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вывод десяти самых популярных тегов и количества постов к ним"""

    serializer_class = serializers.TopTagsSerializer

    def get_queryset(self):
        return caching.get_cached_objects_or_queryset(settings.KEY_ALL_TAGS)


# class CommentListCreateView(APIView):
#     """Получение списка комментариев и добавление нового комментария к заданному посту"""
#
#     def get(self, request: Request):
#         post_id = request.query_params.get('post_id')
#         validators.validate_post_id_param(post_id)
#         comments = queryset.qs_definition(settings.KEY_COMMENTS_LIST, post_id=post_id)
#         serializer = serializers.CommentsSerializer(comments, many=True)
#         return Response(serializer.data)
#
#     def post(self, request: Request) -> Response:
#         comment = serializers.AddCommentSerializer(data=request.data)
#         if comment.is_valid():
#             comment.save()
#             return Response({'message': _('Комментарий успешно добавлен.')}, status=status.HTTP_201_CREATED)
#         return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


# class CommentListCreateView(generics.ListCreateAPIView):
#     """Получение списка комментариев и добавление нового комментария к заданному посту"""
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return serializers.CommentsSerializer
#         elif self.request.method == 'POST':
#             return serializers.AddCommentSerializer
#
#     def get_queryset(self):
#         return queryset.qs_definition(settings.KEY_COMMENTS_LIST, post_id=self.kwargs['post_id'])
#
#     def list(self, request, *args, **kwargs):
#         self.kwargs['post_id'] = request.query_params.get('post_id')
#         validators.validate_post_id_param(self.kwargs['post_id'])
#         return super().list(request, *args, **kwargs)
#
#     def create(self, request, *args, **kwargs):
#         super().create(request, *args, **kwargs)
#         return Response({'message': _('Комментарий успешно добавлен.')}, status=status.HTTP_201_CREATED)


class CommentViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Получение списка комментариев и добавление нового комментария к заданному посту"""

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CommentsSerializer
        elif self.action == 'create':
            return serializers.AddCommentSerializer

    def get_queryset(self):
        return queryset.qs_definition(settings.KEY_COMMENTS_LIST, post_id=self.kwargs['post_id'])

    def list(self, request, *args, **kwargs):
        self.kwargs['post_id'] = request.query_params.get('post_id')
        validators.validate_post_id_param(self.kwargs['post_id'])
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'message': _('Комментарий успешно добавлен.')}, status=status.HTTP_201_CREATED)
