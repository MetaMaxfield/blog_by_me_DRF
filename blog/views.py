import re

from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Mark, Rating
from blog.serializers import (
    AddCommentSerializer,
    AddRatingSerializer,
    CategoryListSerializer,
    PostDetailSerializer,
    PostsSerializer,
    TopTagsSerializer,
    VideoListSerializer,
)
from blog_by_me_DRF import settings
from services import caching, rating, search
from services.blog.paginator import (
    CursorPaginationForPostsInCategoryList,
    LimitOffsetPaginationForVideoList,
    PageNumberPaginationForPosts,
)
from services.client_ip import get_client_ip
from users.models import User


class PostsView(APIView):
    """Вывод постов блога"""

    def get(self, request):
        object_list = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)

        paginator = PageNumberPaginationForPosts()
        paginated_object_list = paginator.paginate_queryset(object_list, request)

        serializer = PostsSerializer(paginated_object_list, many=True)

        return paginator.get_paginated_response(serializer.data)


class SearchPostView(APIView):
    """Вывод результатов поиска постов блога"""

    def get(self, request):

        q = request.query_params.get('q')
        if not q:
            return Response(
                {'detail': _('Пожалуйста, введите текст для поиска постов.')}, status=status.HTTP_400_BAD_REQUEST
            )

        post_list = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)

        post_list = search.search_by_q(q, post_list, request.LANGUAGE_CODE)

        if not post_list.exists():
            return Response(
                {'detail': _('Посты по запросу "{q}" не найдены').format(q=q)}, status=status.HTTP_204_NO_CONTENT
            )

        paginator = PageNumberPaginationForPosts()
        paginated_post_list = paginator.paginate_queryset(post_list, request)

        serializer = PostsSerializer(paginated_post_list, many=True)

        return paginator.get_paginated_response(serializer.data)


class FilterDatePostsView(APIView):
    """Вывод постов с фильтрацией по дате"""

    def get(self, request, date_post):

        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_post):
            return Response({'detail': _('Задан неправильный формат даты')}, status=status.HTTP_400_BAD_REQUEST)

        post_list = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)

        post_list = search.search_by_date(post_list, date_post)

        if not post_list.exists():
            return Response(
                {'detail': _('Посты с датой "{date_post}" не найдены').format(date_post=date_post)},
                status=status.HTTP_204_NO_CONTENT,
            )

        paginator = PageNumberPaginationForPosts()
        paginated_post_list = paginator.paginate_queryset(post_list, request)

        serializer = PostsSerializer(paginated_post_list, many=True)

        return paginator.get_paginated_response(serializer.data)


class FilterTagPostsView(APIView):
    """Вывод постов с фильтрацией по тегу"""

    def get(self, request, tag_slug):
        post_list = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)

        post_list = search.search_by_tag(post_list, tag_slug)

        if not post_list.exists():
            return Response({'detail': _('Посты с заданным тегом не найдены')}, status=status.HTTP_204_NO_CONTENT)

        paginator = PageNumberPaginationForPosts()
        paginated_post_list = paginator.paginate_queryset(post_list, request)

        serializer = PostsSerializer(paginated_post_list, many=True)

        return paginator.get_paginated_response(serializer.data)


class AddCommentView(APIView):
    """Добавление комментария к посту"""

    def post(self, request):
        comment = AddCommentSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
            return Response({'message': _('Комментарий успешно добавлен.')}, status=status.HTTP_201_CREATED)
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """Вывод отдельного поста"""

    def get(self, request, slug):
        post = caching.get_cached_objects_or_queryset(settings.KEY_POST_DETAIL, slug=slug)

        post.user_rating = rating.has_user_rated_post(get_client_ip(request), post)

        serializer = PostDetailSerializer(post)

        return Response(serializer.data)


class CategoryListView(APIView):
    """Вывод списка категорий и постов к ним"""

    def get(self, request):
        category_list = caching.get_cached_objects_or_queryset(settings.KEY_CATEGORIES_LIST)
        post_list = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_LIST)

        paginator = CursorPaginationForPostsInCategoryList()
        paginated_post_list = paginator.paginate_queryset(post_list, request)

        category_serializer = CategoryListSerializer(category_list, many=True)
        posts_serializer = PostsSerializer(paginated_post_list, many=True)

        return paginator.get_paginated_response(
            {
                'category_list': category_serializer.data,
                'post_list': posts_serializer.data,
            }
        )


class VideoListView(APIView):
    """Вывод всех видеозаписей"""

    def get(self, request):
        video_list = caching.get_cached_objects_or_queryset(settings.KEY_VIDEOS_LIST)

        paginator = LimitOffsetPaginationForVideoList()
        paginated_video_list = paginator.paginate_queryset(video_list, request)

        videos_serializer = VideoListSerializer(paginated_video_list, many=True)

        return paginator.get_paginated_response(videos_serializer.data)


class AddRatingView(APIView):
    """Добавление рейтинга к посту"""

    RATING_UPDATE_MESSAGE = _('Рейтинг успешно обновлен.')
    RATING_CREATE_MESSAGE = _('Рейтинг успешно добавлен.')

    def put(self, request):
        # Получаем IP пользователя
        ip = get_client_ip(request)

        # Пытаемся найти существующий рейтинг для поста и пользователя по IP
        # Если рейтинг найден, сериализуем его для обновления
        try:
            rating = Rating.objects.get(ip=ip, post=request.data['post'])
            rating_serializer = AddRatingSerializer(instance=rating, data=request.data)
            status_code, message = status.HTTP_200_OK, self.RATING_UPDATE_MESSAGE

        # Если рейтинга нет, создаем новый сериализатор для нового объекта рейтинга
        except Rating.DoesNotExist:
            rating_serializer = AddRatingSerializer(data=request.data)
            status_code, message = status.HTTP_201_CREATED, self.RATING_CREATE_MESSAGE

        if rating_serializer.is_valid():

            mark = get_object_or_404(Mark, id=request.data['mark'])
            author = get_object_or_404(User, post_author__id=request.data['post'])

            # Если рейтинг обновляется, убираем старое значение
            if message == self.RATING_UPDATE_MESSAGE:
                author.user_rating -= rating.mark.value

            # Прибавляем новое значение рейтинга и сохраняем
            author.user_rating += mark.value
            author.save()

            rating_serializer.save(ip=ip)

            return Response({'message': _(message)}, status=status_code)

        return Response(rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopPostsView(APIView):
    """Вывод трёх постов с наивысшим рейтингом"""

    def get(self, request):
        top_posts = caching.get_cached_objects_or_queryset(settings.KEY_TOP_POSTS)

        serializer = PostsSerializer(top_posts, many=True, fields=('title', 'body', 'url'))

        return Response(serializer.data)


class LastPostsView(APIView):
    """Вывод трех последних опубликованных постов"""

    def get(self, request):
        last_posts = caching.get_cached_objects_or_queryset(settings.KEY_LAST_POSTS)

        serializer = PostsSerializer(last_posts, many=True, fields=('image', 'title', 'body', 'url'))

        return Response(serializer.data)


class DaysInCalendarView(APIView):
    """Вывод дат публикации постов для заданного месяца"""

    def get(self, request, year, month):
        days_with_post = caching.get_cached_objects_or_queryset(settings.KEY_POSTS_CALENDAR, year=year, month=month)

        return Response(days_with_post)


class TopTagsView(APIView):
    """Вывод десяти самых популярных тегов и количества постов к ним"""

    def get(self, request):
        tags = caching.get_cached_objects_or_queryset(settings.KEY_ALL_TAGS)

        serializer = TopTagsSerializer(tags, many=True)

        return Response(serializer.data)
