import pytest

from blog.models import Category


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
