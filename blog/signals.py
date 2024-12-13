from django.db.models.signals import post_delete, pre_save
from django.dispatch.dispatcher import receiver

from blog.models import Post, Video


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


@receiver(post_delete, sender=Video)
def video_file_delete(sender, instance, **kwargs):
    """Удаляет файл с видео при удалении видео в блоге"""
    if instance.file:
        instance.file.delete(save=False)
