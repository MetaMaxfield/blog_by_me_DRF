import pytest
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from blog.models import Category, Post, Video


class CategoryModelTest:
    """Тестирование модели Category"""

    def test_name_verbose_name(self):
        fact_verbose_name = Category._meta.get_field('name').verbose_name
        expected_verbose_name = 'Категория'
        assert fact_verbose_name == expected_verbose_name

    def test_name_max_length(self):
        fact_max_length = Category._meta.get_field('name').max_length
        expected_max_length = 150
        assert fact_max_length == expected_max_length

    def test_description_verbose_name(self):
        fact_verbose_name = Category._meta.get_field('description').verbose_name
        expected_verbose_name = 'Описание'
        assert fact_verbose_name == expected_verbose_name

    def test_url_max_length(self):
        fact_max_length = Category._meta.get_field('url').max_length
        expected_max_length = 160
        assert fact_max_length == expected_max_length

    def test_url_unique(self):
        fact_unique = Category._meta.get_field('url').unique
        expected_unique = True
        assert fact_unique is expected_unique

    @pytest.mark.django_db
    def test_object_name_is_name(self, category):
        fact_object_name = str(category)
        expected_object_name = category.name
        assert fact_object_name == expected_object_name

    def test_model_verbose_name(self):
        fact_verbose_name = Category._meta.verbose_name
        expected_verbose_name = 'Категория'
        assert fact_verbose_name == expected_verbose_name

    def test_model_verbose_name_plural(self):
        fact_verbose_name_plural = Category._meta.verbose_name_plural
        expected_verbose_name_plural = 'Категории'
        assert fact_verbose_name_plural == expected_verbose_name_plural


class VideoModelTest:
    """Тестирование модели Video"""

    def test_title_max_length(self):
        fact_max_length = Video._meta.get_field('title').max_length
        expected_max_length = 100
        assert fact_max_length == expected_max_length

    def test_title_verbose_name(self):
        fact_verbose_name = Video._meta.get_field('title').verbose_name
        expected_verbose_name = 'Заголовок видео'
        assert fact_verbose_name == expected_verbose_name

    def test_description_verbose_name(self):
        fact_verbose_name = Video._meta.get_field('description').verbose_name
        expected_verbose_name = 'Описание видео'
        assert fact_verbose_name == expected_verbose_name

    def test_file_upload_to(self):
        fact_upload_to = Video._meta.get_field('file').upload_to
        expected_upload_to = 'video/'
        assert fact_upload_to == expected_upload_to

    def test_file_validators(self):
        fact_validators = Video._meta.get_field('file').validators
        expected_validators = [FileExtensionValidator(allowed_extensions=['mp4'])]
        assert fact_validators == expected_validators

    def test_file_verbose_name(self):
        fact_verbose_name = Video._meta.get_field('file').verbose_name
        expected_verbose_name = 'Видеофайл'
        assert fact_verbose_name == expected_verbose_name

    def test_create_at_auto_now_add(self):
        fact_auto_now_add = Video._meta.get_field('create_at').auto_now_add
        expected_auto_now_add = True
        assert fact_auto_now_add is expected_auto_now_add

    @pytest.mark.django_db
    def test_object_name_is_title(self, video):
        fact_object_name = str(video)
        expected_object_name = video.title
        assert fact_object_name == expected_object_name

    def test_model_ordering(self):
        fact_ordering = Video._meta.ordering
        expected_ordering = ('-create_at',)
        assert fact_ordering == expected_ordering

    def test_model_verbose_name(self):
        fact_verbose_name = Video._meta.verbose_name
        expected_verbose_name = 'Видеозапись'
        assert fact_verbose_name == expected_verbose_name

    def test_model_verbose_name_plural(self):
        fact_verbose_name_plural = Video._meta.verbose_name_plural
        expected_verbose_name_plural = 'Видеозаписи'
        assert fact_verbose_name_plural == expected_verbose_name_plural


class PostModelTest:
    """Тестирование модели Post"""

    def test_title_verbose_name(self):
        fact_verbose_name = Post._meta.get_field('title').verbose_name
        expected_verbose_name = 'Заголовок'
        assert fact_verbose_name == expected_verbose_name

    def test_title_max_length(self):
        fact_max_length = Post._meta.get_field('title').max_length
        expected_max_length = 250
        assert fact_max_length == expected_max_length

    def test_url_max_length(self):
        fact_max_length = Post._meta.get_field('url').max_length
        expected_max_length = 25
        assert fact_max_length == expected_max_length

    def test_url_unique_for_date(self):
        fact_unique_for_date = Post._meta.get_field('url').unique_for_date
        expected_unique_for_date = 'publish'
        assert fact_unique_for_date == expected_unique_for_date

    def test_url_unique(self):
        fact_unique = Post._meta.get_field('url').unique
        expected_unique = True
        assert fact_unique is expected_unique

    def test_author_to_model(self):
        fact_to_model = Post._meta.get_field('author').remote_field.model
        expected_to_model = get_user_model()
        assert fact_to_model == expected_to_model

    def test_author_verbose_name(self):
        fact_verbose_name = Post._meta.get_field('author').verbose_name
        expected_verbose_name = 'Автор'
        assert fact_verbose_name == expected_verbose_name

    def test_author_on_delete(self):
        fact_on_delete = Post._meta.get_field('author').remote_field.on_delete
        expected_on_delete = models.CASCADE
        assert fact_on_delete == expected_on_delete

    def test_author_related_name(self):
        fact_related_name = Post._meta.get_field('author').remote_field.related_name
        expected_related_name = 'post_author'
        assert fact_related_name == expected_related_name

    def test_author_null(self):
        fact_null = Post._meta.get_field('author').null
        expected_null = True
        assert fact_null is expected_null

    def test_category_to_model(self):
        fact_to_model = Post._meta.get_field('category').remote_field.model
        expected_to_model = Category
        assert fact_to_model == expected_to_model

    def test_category_verbose_name(self):
        fact_verbose_name = Post._meta.get_field('category').verbose_name
        expected_verbose_name = 'Категория'
        assert fact_verbose_name == expected_verbose_name

    def test_category_related_name(self):
        fact_related_name = Post._meta.get_field('category').remote_field.related_name
        expected_related_name = 'post_category'
        assert fact_related_name == expected_related_name

    def test_category_on_delete(self):
        fact_on_delete = Post._meta.get_field('category').remote_field.on_delete
        expected_on_delete = models.SET_NULL
        assert fact_on_delete == expected_on_delete

    def test_category_null(self):
        fact_null = Post._meta.get_field('category').null
        expected_null = True
        assert fact_null is expected_null

    def test_tags_related_name(self):
        fact_related_name = Post._meta.get_field('tags').remote_field.related_name
        expected_related_name = 'post_tags'
        assert fact_related_name == expected_related_name

    def test_body_verbose_name(self):
        fact_verbose_name = Post._meta.get_field('body').verbose_name
        expected_verbose_name = 'Содержание'
        assert fact_verbose_name == expected_verbose_name

    def test_video_to_model(self):
        fact_to_model = Post._meta.get_field('video').remote_field.model
        expected_to_model = Video
        assert fact_to_model == expected_to_model

    def test_video_verbose_name(self):
        fact_verbose_name = Post._meta.get_field('video').verbose_name
        expected_verbose_name = 'Видео к записи'
        assert fact_verbose_name == expected_verbose_name

    def test_video_related_name(self):
        fact_related_name = Post._meta.get_field('video').remote_field.related_name
        expected_related_name = 'post_video'
        assert fact_related_name == expected_related_name

    def test_video_on_delete(self):
        fact_on_delete = Post._meta.get_field('video').remote_field.on_delete
        expected_on_delete = models.SET_NULL
        assert fact_on_delete == expected_on_delete

    def test_video_null(self):
        fact_null = Post._meta.get_field('video').null
        expected_null = True
        assert fact_null is expected_null

    def test_video_blank(self):
        fact_blank = Post._meta.get_field('video').blank
        expected_blank = True
        assert fact_blank is expected_blank

    def test_image_verbose_name(self):
        fact_verbose_name = Post._meta.get_field('image').verbose_name
        expected_verbose_name = 'Изображение'
        assert fact_verbose_name == expected_verbose_name

    def test_image_upload_to(self):
        fact_upload_to = Post._meta.get_field('image').upload_to
        expected_upload_to = 'posts/'
        assert fact_upload_to == expected_upload_to

    def test_publish_default(self):
        fact_default = Post._meta.get_field('publish').default
        expected_default = timezone.now
        assert fact_default == expected_default

    def test_publish_help_text(self):
        fact_help_text = Post._meta.get_field('publish').help_text
        expected_help_text = (
            'Укажите дату и время, когда пост должен быть опубликован. '
            'Оставьте текущую дату и время для немедленной публикации, '
            'либо выберите будущую дату для отложенного поста. '
            'Обратите внимание: изменить время публикации можно будет только '
            'до наступления ранее указанного времени.'
        )
        assert fact_help_text == expected_help_text

    def test_publish_verbose_name(self):
        fact_verbose_name = Post._meta.get_field('publish').verbose_name
        expected_verbose_name = 'Время публикации'
        assert fact_verbose_name == expected_verbose_name

    def test_created_auto_now_add(self):
        fact_auto_now_add = Post._meta.get_field('created').auto_now_add
        expected_auto_now_add = True
        assert fact_auto_now_add is expected_auto_now_add

    def test_updated_auto_now(self):
        fact_auto_now = Post._meta.get_field('updated').auto_now
        expected_auto_now = True
        assert fact_auto_now is expected_auto_now

    def test_draft_default(self):
        fact_default = Post._meta.get_field('draft').default
        expected_default = False
        assert fact_default is expected_default

    def test_draft_verbose_name(self):
        fact_verbose_name = Post._meta.get_field('draft').verbose_name
        expected_verbose_name = 'Черновик'
        assert fact_verbose_name == expected_verbose_name

    @pytest.mark.django_db
    def test_object_name_is_title(self, post):
        fact_object_name = str(post)
        expected_object_name = post.title
        assert fact_object_name == expected_object_name

    def test_model_verbose_name(self):
        fact_verbose_name = Post._meta.verbose_name
        expected_verbose_name = 'Пост'
        assert fact_verbose_name == expected_verbose_name

    def test_model_verbose_name_plural(self):
        fact_verbose_name_plural = Post._meta.verbose_name_plural
        expected_verbose_name_plural = 'Посты'
        assert fact_verbose_name_plural == expected_verbose_name_plural

    def test_model_indexes(self):
        fact_indexes = Post._meta.indexes
        expected_indexes = [
            models.Index(fields=('-publish', '-id'), name='publish_id_idx'),
        ]
        assert fact_indexes == expected_indexes

    def test_model_ordering(self):
        fact_ordering = Post._meta.ordering
        expected_ordering = ('-publish', '-id')
        assert fact_ordering == expected_ordering
