from django.core.cache import cache
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch.dispatcher import receiver

from blog.models import Post, Video
from blog_by_me_DRF import settings


def _clear_cache_post(instance: Post) -> None:
    """Функция для очистки кэша с данными постов"""

    # Список ключей для кэширования объектов, которые нужно очистить
    keys_list_objects = [
        f'{settings.KEY_POSTS_LIST}',
        f'{settings.KEY_LAST_POSTS}',
        f'{settings.KEY_POST_DETAIL}{instance.url}',
        f'{settings.KEY_AUTHOR_DETAIL}{instance.author.id}',
    ]
    # Если у поста есть видео, добавляем ключ для кэширования видеозаписей в список для очистки кэша
    if instance.video:
        keys_list_objects.append(f'{settings.KEY_VIDEOS_LIST}')

    # Удаляем кэш для каждого ключа из списка
    for key in keys_list_objects:
        cache.delete(f'{settings.CACHE_KEY}{key}')


@receiver(post_delete, sender=Post)
def clear_cache_when_deleting_post(sender, instance, **kwargs):
    """Вызывает функцию для удаления старых данных из кэша при удалении поста"""
    _clear_cache_post(instance)


@receiver(post_delete, sender=Post)
def post_image_file_delete(sender, instance, **kwargs):
    """Удаляет файл с изображением при удалении поста"""
    if instance.image:
        instance.image.delete(save=False)


@receiver(pre_save, sender=Post)
def post_image_file_delete_when_replace(sender, instance, **kwargs):
    """Удаляет старый файл с изображением при изменении картинки в посте"""
    if instance.id:
        old_instance = Post.objects.get(id=instance.id)
        if old_instance.image != instance.image:
            old_instance.image.delete(save=False)


@receiver(post_save, sender=Post)
def clear_cache_when_draft_post(sender, instance, **kwargs):
    """Вызывает функцию для удаления старых данных из кэша при скрытии поста поста (draft=True)"""
    if instance.draft:
        _clear_cache_post(instance)


@receiver(post_delete, sender=Video)
def video_file_delete(sender, instance, **kwargs):
    """Удаляет файл с видео при удалении видео в блоге"""
    if instance.file:
        instance.file.delete(save=False)
