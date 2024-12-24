import re

from django.core.cache import cache
from django.db.models import Count, Prefetch, Q, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag, TaggedItem

from blog.models import Category, Comment, Mark, Post, Rating, Video
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
from services import rating, search
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

        object_list = cache.get(f'{settings.CACHE_KEY}{settings.KEY_POSTS_LIST}')

        if not object_list:

            object_list = (
                Post.objects.filter(draft=False, publish__lte=timezone.now())
                .select_related('category')
                .prefetch_related(
                    Prefetch(
                        'tagged_items', queryset=TaggedItem.objects.select_related('tag'), to_attr='prefetched_tags'
                    ),
                    Prefetch('author', User.objects.only('id', 'username')),
                )
                .defer('video', 'created', 'updated', 'draft')
                .annotate(ncomments=Count('comments'))
                .order_by('-publish', '-id')
            )

            cache.set(
                key=f'{settings.CACHE_KEY}{settings.KEY_POSTS_LIST}',
                value=object_list,
                timeout=settings.CACHE_TIMES[settings.KEY_POSTS_LIST],
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
                {'detail': _('Пожалуйста, введите текст для поиска постов.')}, status=status.HTTP_400_BAD_REQUEST
            )

        post_list = cache.get(f'{settings.CACHE_KEY}{settings.KEY_POSTS_LIST}')

        if not post_list:

            post_list = (
                Post.objects.filter(draft=False, publish__lte=timezone.now())
                .select_related('category')
                .prefetch_related(
                    Prefetch(
                        'tagged_items', queryset=TaggedItem.objects.select_related('tag'), to_attr='prefetched_tags'
                    ),
                    Prefetch('author', User.objects.only('id', 'username')),
                )
                .defer('video', 'created', 'updated', 'draft')
                .annotate(ncomments=Count('comments'))
            )

            cache.set(
                key=f'{settings.CACHE_KEY}{settings.KEY_POSTS_LIST}',
                value=post_list,
                timeout=settings.CACHE_TIMES[settings.KEY_POSTS_LIST],
            )

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

        post_list = cache.get(f'{settings.CACHE_KEY}{settings.KEY_POSTS_LIST}')

        if not post_list:

            post_list = (
                Post.objects.filter(draft=False, publish__lte=timezone.now())
                .select_related('category')
                .prefetch_related(
                    Prefetch(
                        'tagged_items', queryset=TaggedItem.objects.select_related('tag'), to_attr='prefetched_tags'
                    ),
                    Prefetch('author', User.objects.only('id', 'username')),
                )
                .defer('video', 'created', 'updated', 'draft')
                .annotate(ncomments=Count('comments'))
                .order_by('-publish', '-id')
            )

            cache.set(
                key=f'{settings.CACHE_KEY}{settings.KEY_POSTS_LIST}',
                value=post_list,
                timeout=settings.CACHE_TIMES[settings.KEY_POSTS_LIST],
            )

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

        post_list = cache.get(f'{settings.CACHE_KEY}{settings.KEY_POSTS_LIST}')

        if not post_list:

            post_list = (
                Post.objects.filter(draft=False, publish__lte=timezone.now())
                .select_related('category')
                .prefetch_related(
                    Prefetch(
                        'tagged_items', queryset=TaggedItem.objects.select_related('tag'), to_attr='prefetched_tags'
                    ),
                    Prefetch('author', User.objects.only('id', 'username')),
                )
                .defer('video', 'created', 'updated', 'draft')
                .annotate(ncomments=Count('comments'))
                .order_by('-publish', '-id')
            )

            cache.set(
                key=f'{settings.CACHE_KEY}{settings.KEY_POSTS_LIST}',
                value=post_list,
                timeout=settings.CACHE_TIMES[settings.KEY_POSTS_LIST],
            )

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

        post = cache.get(f'{settings.CACHE_KEY}{settings.KEY_POST_DETAIL}{slug}')

        if not post:
            post = get_object_or_404(
                Post.objects.filter(draft=False, publish__lte=timezone.now())
                .prefetch_related(
                    Prefetch('author', User.objects.only('id', 'username')),
                    Prefetch(
                        'comments',
                        Comment.objects.filter(parent=None)
                        .prefetch_related(
                            Prefetch(
                                'children', Comment.objects.defer('email', 'active'), to_attr='prefetched_comments2'
                            )
                        )
                        .defer('email', 'active'),
                        to_attr='prefetched_comments1',
                    ),
                )
                .defer('draft')
                .annotate(
                    ncomments=Count('comments'),
                ),
                url=slug,
            )

            cache.set(
                key=f'{settings.CACHE_KEY}{settings.KEY_POST_DETAIL}{slug}',
                value=post,
                timeout=settings.CACHE_TIMES[settings.KEY_POST_DETAIL],
            )

        post.user_rating = rating.has_user_rated_post(get_client_ip(request), post)

        serializer = PostDetailSerializer(post)

        return Response(serializer.data)


class CategoryListView(APIView):
    """Вывод списка категорий и постов к ним"""

    def get(self, request):

        category_list = cache.get(f'{settings.CACHE_KEY}{settings.KEY_CATEGORIES_LIST}')

        if not category_list:
            category_list = Category.objects.all()
            cache.set(
                key=f'{settings.CACHE_KEY}{settings.KEY_CATEGORIES_LIST}',
                value=category_list,
                timeout=settings.CACHE_TIMES[settings.KEY_CATEGORIES_LIST],
            )

        post_list = cache.get(f'{settings.CACHE_KEY}{settings.KEY_POSTS_LIST}')

        if not post_list:

            post_list = (
                Post.objects.filter(draft=False, publish__lte=timezone.now())
                .select_related('category')
                .prefetch_related(
                    Prefetch(
                        'tagged_items', queryset=TaggedItem.objects.select_related('tag'), to_attr='prefetched_tags'
                    ),
                    Prefetch('author', User.objects.only('id', 'username')),
                )
                .defer('video', 'created', 'updated', 'draft')
                .annotate(ncomments=Count('comments'))
                .order_by('-publish', '-id')
            )

            cache.set(
                key=f'{settings.CACHE_KEY}{settings.KEY_POSTS_LIST}',
                value=post_list,
                timeout=settings.CACHE_TIMES[settings.KEY_POSTS_LIST],
            )

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

        video_list = cache.get(f'{settings.CACHE_KEY}{settings.KEY_VIDEOS_LIST}')

        if not video_list:

            video_list = (
                Video.objects.filter(post_video__draft=False, post_video__publish__lte=timezone.now())
                .select_related('post_video')
                .prefetch_related(
                    Prefetch('post_video__category', Category.objects.only('id', 'name')),
                    Prefetch('post_video__author', User.objects.only('id', 'username')),
                    Prefetch(
                        'post_video__tagged_items',
                        queryset=TaggedItem.objects.select_related('tag'),
                        to_attr='prefetched_tags',
                    ),
                )
                .annotate(
                    ncomments=Count('post_video__comments'),
                )
                .order_by('-create_at')
            )

            cache.set(
                key=f'{settings.CACHE_KEY}{settings.KEY_VIDEOS_LIST}',
                value=video_list,
                timeout=settings.CACHE_TIMES[settings.KEY_VIDEOS_LIST],
            )

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

        top_posts = cache.get(f'{settings.CACHE_KEY}{settings.KEY_TOP_POSTS}')

        if not top_posts:

            top_posts = (
                Post.objects.filter(draft=False, publish__lte=timezone.now())
                .only('title', 'body', 'url')
                .alias(total_likes=Coalesce(Sum('rating_post__mark__value'), 0))
                .order_by('-total_likes')[:3]
            )

            cache.set(
                key=f'{settings.CACHE_KEY}{settings.KEY_TOP_POSTS}',
                value=top_posts,
                timeout=settings.CACHE_TIMES[settings.KEY_TOP_POSTS],
            )

        serializer = PostsSerializer(top_posts, many=True, fields=('title', 'body', 'url'))

        return Response(serializer.data)


class LastPostsView(APIView):
    """Вывод трех последних опубликованных постов"""

    def get(self, request):

        last_posts = cache.get(f'{settings.CACHE_KEY}{settings.KEY_LAST_POSTS}')

        if not last_posts:

            last_posts = (
                Post.objects.filter(draft=False, publish__lte=timezone.now())
                .only('image', 'title', 'body', 'url')
                .order_by('-publish', '-id')[:3]
            )

            cache.set(
                key=f'{settings.CACHE_KEY}{settings.KEY_LAST_POSTS}',
                value=last_posts,
                timeout=settings.CACHE_TIMES[settings.KEY_LAST_POSTS],
            )

        serializer = PostsSerializer(last_posts, many=True, fields=('image', 'title', 'body', 'url'))

        return Response(serializer.data)


class DaysInCalendarView(APIView):
    """Вывод дат публикации постов для заданного месяца"""

    def get(self, request, year, month):

        days_with_post = cache.get(f'{settings.CACHE_KEY}{settings.KEY_POSTS_CALENDAR}')

        if not days_with_post:

            days_with_post = Post.objects.filter(
                draft=False, publish__lte=timezone.now(), publish__year=year, publish__month=month
            ).dates('publish', 'day')

            cache.set(
                key=f'{settings.CACHE_KEY}{settings.KEY_POSTS_CALENDAR}',
                value=days_with_post,
                timeout=settings.CACHE_TIMES[settings.KEY_POSTS_CALENDAR],
            )

        return Response(days_with_post)


class TopTagsView(APIView):
    """Вывод десяти самых популярных тегов и количества постов к ним"""

    def get(self, request):

        tags = cache.get(f'{settings.CACHE_KEY}{settings.KEY_ALL_TAGS}')

        if not tags:

            tags = Tag.objects.annotate(
                npost=Count('post_tags', filter=Q(post_tags__draft=False, post_tags__publish__lte=timezone.now()))
            ).order_by('-npost')[:10]

            cache.set(
                key=f'{settings.CACHE_KEY}{settings.KEY_ALL_TAGS}',
                value=tags,
                timeout=settings.CACHE_TIMES[settings.KEY_ALL_TAGS],
            )

        serializer = TopTagsSerializer(tags, many=True)

        return Response(serializer.data)
