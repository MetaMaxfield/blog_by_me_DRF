import datetime
import re

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Count, OuterRef, Prefetch, Q, Subquery, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import CursorPagination, LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag

from blog.models import Category, Post, Rating, Video
from blog.serializers import (
    AddCommentSerializer,
    AddRatingSerializer,
    CategoryListSerializer,
    PostDetailSerializer,
    PostsSerializer,
    TopTagsSerializer,
    VideoListSerializer,
)


def get_client_ip(request):
    """Получение IP пользоваетля"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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


class PostsView(APIView):
    """Вывод постов блога"""

    def get(self, request):
        object_list = (
            Post.objects.filter(draft=False, publish__lte=timezone.now())
            .select_related('category')
            .prefetch_related(
                'tagged_items__tag',
            )
            .defer('video', 'created', 'updated', 'draft')
            .annotate(ncomments=Count('comments'))
            .order_by('-publish', '-id')
        )
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
                {'detail': 'Пожалуйста, введите текст для поиска постов.'}, status=status.HTTP_400_BAD_REQUEST
            )
        post_list = (
            Post.objects.filter(draft=False, publish__lte=timezone.now())
            .select_related('category')
            .prefetch_related(
                'tagged_items__tag',
            )
            .defer('video', 'created', 'updated', 'draft')
            .annotate(ncomments=Count('comments'))
        )
        search_vector = SearchVector('title', 'body')
        search_query = SearchQuery(q)
        post_list = (
            post_list.annotate(search=search_vector, rank=SearchRank(search_vector, search_query))
            .filter(search=search_query)
            .order_by('-rank')
        )
        if not post_list.exists():
            return Response({'detail': f'Посты по запросу "{q}" не найдены'}, status=status.HTTP_204_NO_CONTENT)
        paginator = PageNumberPaginationForPosts()
        paginated_post_list = paginator.paginate_queryset(post_list, request)
        serializer = PostsSerializer(paginated_post_list, many=True)
        return paginator.get_paginated_response(serializer.data)


class FilterDatePostsView(APIView):
    """Вывод постов с фильтрацией по дате"""

    def get(self, request, date_post):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_post):
            return Response({'detail': 'Задан неправильный формат даты'}, status=status.HTTP_400_BAD_REQUEST)
        date_post = datetime.datetime.strptime(date_post, '%Y-%m-%d').date()
        post_list = (
            Post.objects.filter(draft=False, publish__lte=timezone.now())
            .select_related('category')
            .prefetch_related(
                'tagged_items__tag',
            )
            .defer('video', 'created', 'updated', 'draft')
            .annotate(ncomments=Count('comments'))
            .order_by('-publish', '-id')
        )
        post_list = post_list.filter(created__date=date_post)
        if not post_list.exists():
            return Response({'detail': f'Посты с датой {date_post} не найдены'}, status=status.HTTP_204_NO_CONTENT)
        paginator = PageNumberPaginationForPosts()
        paginated_post_list = paginator.paginate_queryset(post_list, request)
        serializer = PostsSerializer(paginated_post_list, many=True)
        return paginator.get_paginated_response(serializer.data)


class FilterTagPostsView(APIView):
    """Вывод постов с фильтрацией по тегу"""

    def get(self, request, tag_slug):
        post_list = (
            Post.objects.filter(draft=False, publish__lte=timezone.now())
            .select_related('category')
            .prefetch_related(
                'tagged_items__tag',
            )
            .defer('video', 'created', 'updated', 'draft')
            .annotate(ncomments=Count('comments'))
            .order_by('-publish', '-id')
        )
        post_list = post_list.filter(tags__slug=tag_slug)
        if not post_list.exists():
            return Response({'detail': 'Посты с заданным тегом не найдены'}, status=status.HTTP_204_NO_CONTENT)
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
            return Response({'message': 'Комментарий успешно добавлен.'}, status=status.HTTP_201_CREATED)
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """Вывод отдельного поста"""

    def get(self, request, slug):
        ip = get_client_ip(request)
        post = get_object_or_404(
            Post.objects.filter(draft=False, publish__lte=timezone.now())
            .defer('draft')
            .annotate(
                ncomments=Count('comments'),
                user_rating=Subquery(Rating.objects.filter(ip=ip, post=OuterRef('pk')).values('mark__value')),
            ),
            url=slug,
        )
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)


class CategoryListView(APIView):
    """Вывод списка категорий и постов к ним"""

    def get(self, request):
        category_list = Category.objects.all()
        category_serializer = CategoryListSerializer(category_list, many=True)
        post_list = (
            Post.objects.filter(draft=False, publish__lte=timezone.now())
            .select_related('category')
            .prefetch_related(
                'tagged_items__tag',
            )
            .defer('video', 'created', 'updated', 'draft')
            .annotate(ncomments=Count('comments'))
            .order_by('-publish', '-id')
        )
        paginator = CursorPaginationForPostsInCategoryList()
        paginated_post_list = paginator.paginate_queryset(post_list, request)
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
        video_list = (
            Video.objects.filter(post_video__draft=False, post_video__publish__lte=timezone.now())
            .select_related('post_video')
            .prefetch_related(
                Prefetch('post_video__category', Category.objects.only('id', 'name')),
            )
            .annotate(
                ncomments=Count('post_video__comments'),
            )
            .order_by('-create_at')
        )
        paginator = LimitOffsetPaginationForVideoList()
        paginated_video_list = paginator.paginate_queryset(video_list, request)
        videos_serializer = VideoListSerializer(paginated_video_list, many=True)
        return paginator.get_paginated_response(videos_serializer.data)


class AddRatingView(APIView):
    """Добавление рейтинга к посту"""

    def put(self, request):
        ip = get_client_ip(request)

        try:
            rating = AddRatingSerializer(
                instance=Rating.objects.get(ip=ip, post=request.data['post']), data=request.data
            )
            status_code, message = status.HTTP_200_OK, 'Рейтинг успешно обновлен.'
        except Rating.DoesNotExist:
            rating = AddRatingSerializer(data=request.data)
            status_code, message = status.HTTP_201_CREATED, 'Рейтинг успешно добавлен.'

        if rating.is_valid():
            rating.save(ip=ip)
            return Response({'message': message}, status=status_code)

        return Response(rating.errors, status=status.HTTP_400_BAD_REQUEST)


class TopPostsView(APIView):
    """Вывод трёх постов с наивысшим рейтингом"""

    def get(self, request):
        top_posts = (
            Post.objects.filter(draft=False, publish__lte=timezone.now())
            .only('title', 'body', 'url')
            .alias(total_likes=Coalesce(Sum('rating_post__mark__value'), 0))
            .order_by('-total_likes')[:3]
        )
        serializer = PostsSerializer(top_posts, many=True, fields=('title', 'body', 'url'))
        return Response(serializer.data)


class LastPostsView(APIView):
    """Вывод трех последних опубликованных постов"""

    def get(self, request):
        last_posts = (
            Post.objects.filter(draft=False, publish__lte=timezone.now())
            .only('image', 'title', 'body', 'url')
            .order_by('-publish', '-id')[:3]
        )
        serializer = PostsSerializer(last_posts, many=True, fields=('image', 'title', 'body', 'url'))
        return Response(serializer.data)


class DaysInCalendarView(APIView):
    """Вывод дат публикации постов для заданного месяца"""

    def get(self, request, year, month):
        days_with_post = Post.objects.filter(
            draft=False, publish__lte=timezone.now(), publish__year=year, publish__month=month
        ).dates('publish', 'day')
        return Response(days_with_post)


class TopTagsView(APIView):
    """Вывод десяти самых популярных тегов и количества постов к ним"""

    def get(self, request):
        tags = Tag.objects.annotate(
            npost=Count('post_tags', filter=Q(post_tags__draft=False, post_tags__publish__lte=timezone.now()))
        ).order_by('-npost')[:10]
        serializer = TopTagsSerializer(tags, many=True)
        return Response(serializer.data)
