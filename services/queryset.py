from django.db.models import Count, Prefetch, Q, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework.generics import get_object_or_404
from taggit.models import Tag, TaggedItem

from blog.models import Category, Comment, Post, Video
from blog_by_me_DRF import settings
from company.models import About
from users.models import User


def _qs_post_list():
    """Общий QS с записями блога"""

    return (
        Post.objects.filter(draft=False, publish__lte=timezone.now())
        .select_related('category')
        .prefetch_related(
            Prefetch('tagged_items', queryset=TaggedItem.objects.select_related('tag'), to_attr='prefetched_tags'),
            Prefetch('author', User.objects.only('id', 'username')),
        )
        .defer('video', 'created', 'updated', 'draft')
        .annotate(ncomments=Count('comments'))
        .order_by('-publish', '-id')
    )


def _qs_post_detail(slug):
    """Отдельная запись в блоге"""

    return get_object_or_404(
        Post.objects.filter(draft=False, publish__lte=timezone.now())
        .prefetch_related(
            Prefetch('author', User.objects.only('id', 'username')),
            Prefetch(
                'comments',
                Comment.objects.filter(parent=None)
                .prefetch_related(
                    Prefetch('children', Comment.objects.defer('email', 'active'), to_attr='prefetched_comments2')
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


def _qs_categories_list():
    """QS со списком категорий"""

    return Category.objects.all()


def _qs_videos_list():
    """QS со всеми видеозаписями"""

    return (
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


def _qs_about():
    """
    Получение данных страницы 'О нас'
    """

    return get_object_or_404(About)


def _qs_author_list():
    """QS со всеми пользователями"""

    return User.objects.all().only('id', 'username', 'image', 'description')


def _qs_author_detail(pk):
    """QS с отдельным автором"""

    return get_object_or_404(
        User.objects.annotate(
            nposts=Count('post_author', filter=Q(post_author__draft=False, post_author__publish__lte=timezone.now()))
        )
        .prefetch_related(
            Prefetch(
                'post_author',
                Post.objects.filter(draft=False, publish__lte=timezone.now())
                .order_by('-publish', '-id')
                .select_related('category')
                .prefetch_related(
                    Prefetch('tagged_items', TaggedItem.objects.select_related('tag'), to_attr='prefetched_tags')
                )[:3],
                to_attr='last_3_posts',
            )
        )
        .defer('password', 'last_login', 'is_active', 'is_staff'),
        id=pk,
    )


def _qs_top_posts():
    """QS с тремя самыми популярными постами"""

    return (
        Post.objects.filter(draft=False, publish__lte=timezone.now())
        .only('title', 'body', 'url')
        .alias(total_likes=Coalesce(Sum('rating_post__mark__value'), 0))
        .order_by('-total_likes')[:3]
    )


def _qs_last_posts():
    """QS с последними тремя добавленными постами"""

    return (
        Post.objects.filter(draft=False, publish__lte=timezone.now())
        .only('image', 'title', 'body', 'url')
        .order_by('-publish', '-id')[:3]
    )


def _qs_top_tags():
    """QS с десятью популярными тегами по количеству использования"""

    return Tag.objects.annotate(
        npost=Count('post_tags', filter=Q(post_tags__draft=False, post_tags__publish__lte=timezone.now()))
    ).order_by('-npost')[:10]


def _qs_days_posts_in_current_month(year, month):
    """Дни публикаций в заданном месяце для календаря"""

    return Post.objects.filter(
        draft=False, publish__lte=timezone.now(), publish__year=year, publish__month=month
    ).dates('publish', 'day')


def not_definite_qs(**kwargs):
    """Вызов исключения если ключ для получения queryset не найден"""
    raise Exception('Ключ для получения queryset не найден.')


def qs_definition(qs_key, **kwargs):
    """Определение необходимого запроса в БД по ключу"""
    qs_keys = {
        settings.KEY_POSTS_LIST: _qs_post_list,
        settings.KEY_POST_DETAIL: _qs_post_detail,
        settings.KEY_CATEGORIES_LIST: _qs_categories_list,
        settings.KEY_VIDEOS_LIST: _qs_videos_list,
        settings.KEY_ABOUT: _qs_about,
        settings.KEY_AUTHORS_LIST: _qs_author_list,
        settings.KEY_AUTHOR_DETAIL: _qs_author_detail,
        settings.KEY_TOP_POSTS: _qs_top_posts,
        settings.KEY_LAST_POSTS: _qs_last_posts,
        settings.KEY_ALL_TAGS: _qs_top_tags,
        settings.KEY_POSTS_CALENDAR: _qs_days_posts_in_current_month,
    }
    definite_qs = qs_keys.get(qs_key, not_definite_qs)
    return definite_qs(**kwargs) if kwargs else definite_qs()
