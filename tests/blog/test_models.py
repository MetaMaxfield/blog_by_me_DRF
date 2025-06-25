import pytest
from django.core.validators import FileExtensionValidator

from blog.models import Category, Video


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
