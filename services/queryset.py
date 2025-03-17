from typing import Any, NoReturn, Union

from django.db.models import Count, Prefetch, Q, QuerySet, Sum
from django.db.models.functions import Coalesce
from django.http import Http404
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from taggit.models import Tag, TaggedItem

from blog.models import Category, Comment, Mark, Post, Rating, Video
from blog_by_me_DRF import settings
from company.models import About
from users.models import User


def _qs_post_list() -> QuerySet:
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


def _qs_post_detail(slug: str) -> Post:
    """Отдельная запись в блоге"""
    return get_object_or_404(
        Post.objects.filter(draft=False, publish__lte=timezone.now())
        .prefetch_related(
            Prefetch('author', User.objects.only('id', 'username')),
        )
        .defer('draft')
        .annotate(
            ncomments=Count('comments'),
        ),
        url=slug,
    )


def _qs_rating_detail(ip: str, post_slug: str, http_method: str) -> Rating | None:
    """
    Возвращает текущий рейтинг пользователя к посту, если он существует в базе данных.
    В случае его отсутствия, в зависимости от HTTP-метода запроса:
        - Для POST-запросов (create/update) возвращает None, позволяя создать новый рейтинг
        - Для GET-запросов (retrieve) предполагает вызов исключения (Http404), если рейтинг не найден
    """
    try:
        rating = Rating.objects.get(ip=ip, post__url=post_slug, post__draft=False, post__publish__lte=timezone.now())
    except Rating.DoesNotExist:
        if http_method == 'GET':
            raise Http404
        rating = None
    return rating


def _qs_mark_detail(pk: int) -> Mark:
    """
    Возвращает объект оценки (Mark) по указанному ID.
    Если оценка не найдена, вызывает исключение ValidationError
    """
    try:
        return Mark.objects.get(id=pk)
    except Mark.DoesNotExist:
        raise ValidationError({'detail': _('Оценка с указанным id не найдена.')})


def _qs_categories_list() -> QuerySet:
    """QS со списком категорий"""
    return Category.objects.all()


def _qs_videos_list() -> QuerySet:
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


def _qs_about() -> About:
    """
    Получение данных страницы 'О нас'
    """
    return get_object_or_404(About)


def _qs_author_list() -> QuerySet:
    """QS со всеми пользователями"""
    return User.objects.all().only('id', 'username', 'image', 'description')


def _qs_author_detail(pk: int) -> User:
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


def _qs_top_posts() -> QuerySet:
    """QS с тремя самыми популярными постами"""
    return (
        Post.objects.filter(draft=False, publish__lte=timezone.now())
        .only('title', 'body', 'url')
        .alias(total_likes=Coalesce(Sum('rating_post__mark__value'), 0))
        .order_by('-total_likes')[:3]
    )


def _qs_last_posts() -> QuerySet:
    """QS с последними тремя добавленными постами"""
    return (
        Post.objects.filter(draft=False, publish__lte=timezone.now())
        .only('image', 'title', 'body', 'url')
        .order_by('-publish', '-id')[:3]
    )


def _qs_top_tags() -> QuerySet:
    """QS с десятью популярными тегами по количеству использования"""
    return Tag.objects.annotate(
        npost=Count('post_tags', filter=Q(post_tags__draft=False, post_tags__publish__lte=timezone.now()))
    ).order_by('-npost')[:10]


def _qs_days_posts_in_current_month(year: int, month: int) -> QuerySet:
    """Дни публикаций в заданном месяце для календаря"""
    return Post.objects.filter(
        draft=False, publish__lte=timezone.now(), publish__year=year, publish__month=month
    ).dates('publish', 'day')


def _qs_comments_list(post_id: str) -> QuerySet:
    """QS с комментариями заданного поста"""
    return (
        Comment.objects.filter(post_id=post_id, parent=None)
        .prefetch_related(
            Prefetch('children', Comment.objects.defer('email', 'active'), to_attr='prefetched_comments2')
        )
        .defer('email', 'active')
    )


def not_definite_qs(**kwargs: Any) -> NoReturn:
    """Вызов исключения если ключ для получения queryset не найден"""
    raise Exception('Ключ для получения queryset не найден.')


def qs_definition(qs_key: str, **kwargs: str | int) -> Union[QuerySet, settings.ObjectModel, NoReturn]:
    """Определение необходимого запроса в БД по ключу"""
    qs_keys = {
        settings.KEY_POSTS_LIST: _qs_post_list,
        settings.KEY_POST_DETAIL: _qs_post_detail,
        settings.KEY_RATING_DETAIL: _qs_rating_detail,
        settings.KEY_MARK_DETAIL: _qs_mark_detail,
        settings.KEY_CATEGORIES_LIST: _qs_categories_list,
        settings.KEY_VIDEOS_LIST: _qs_videos_list,
        settings.KEY_ABOUT: _qs_about,
        settings.KEY_AUTHORS_LIST: _qs_author_list,
        settings.KEY_AUTHOR_DETAIL: _qs_author_detail,
        settings.KEY_TOP_POSTS: _qs_top_posts,
        settings.KEY_LAST_POSTS: _qs_last_posts,
        settings.KEY_ALL_TAGS: _qs_top_tags,
        settings.KEY_POSTS_CALENDAR: _qs_days_posts_in_current_month,
        settings.KEY_COMMENTS_LIST: _qs_comments_list,
    }
    definite_qs = qs_keys.get(qs_key, not_definite_qs)
    return definite_qs(**kwargs) if kwargs else definite_qs()
