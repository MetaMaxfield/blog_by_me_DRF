from unittest import mock

import pytest

from blog.models import Rating
from blog.serializers import AddRatingSerializer
from blog_by_me_DRF.settings import KEY_SIMPLE_POSTS_LIST
from tests.blog.factories import RatingFactory


class AddRatingSerializerTest:
    """Тестирование сериализатора AddRatingSerializer(ModelSerializer)"""

    def test_post_slug_field(self):
        fact_slug_field = AddRatingSerializer().fields['post'].slug_field
        expected_slug_field = 'url'
        assert fact_slug_field == expected_slug_field

    @pytest.mark.django_db
    @mock.patch('services.queryset.timezone.now')
    def test_post_queryset(self, mock_timezone_now, filtered_posts_and_timezone_now):
        mock_timezone_now.return_value = filtered_posts_and_timezone_now['time_now']
        fact_queryset = list(AddRatingSerializer().fields['post'].queryset)
        expected_queryset = list(filtered_posts_and_timezone_now['filtered_posts'])
        assert fact_queryset == expected_queryset

    @mock.patch('blog.serializers.qs_definition')
    def test_serializer_init(self, mock_qs_definition):
        _ = AddRatingSerializer()
        mock_qs_definition.assert_called_once_with(KEY_SIMPLE_POSTS_LIST)

    @pytest.mark.django_db
    def test_to_internal_value(self, post, marks):
        post_slug = post.url
        data = {'mark': marks['Лайк'].id}

        internal = AddRatingSerializer(context={'slug': post_slug}).to_internal_value(data)
        assert internal['mark'] == marks['Лайк']
        assert internal['post'] == post

    @pytest.mark.django_db
    def test_create(self, post, marks):
        post_slug = post.url
        ip = '128.0.0.1'
        data = {'mark': marks['Лайк'].id}

        serializer = AddRatingSerializer(data=data, context={'slug': post_slug})
        serializer.is_valid(raise_exception=True)
        serializer.save(ip=ip)
        assert Rating.objects.filter(ip=ip, mark=marks['Лайк']).exists() is True

    @pytest.mark.django_db
    def test_update(self, post, marks):
        post_slug = post.url
        ip = '128.0.0.1'
        rating = RatingFactory(ip=ip, mark=marks['Дизлайк'], post=post)
        data = {'mark': marks['Лайк'].id}

        serializer = AddRatingSerializer(instance=rating, data=data, context={'slug': post_slug})
        serializer.is_valid(raise_exception=True)
        serializer.save(ip=ip)
        assert Rating.objects.filter(ip=ip, mark=marks['Лайк']).exists() is True
        assert Rating.objects.filter(ip=ip, mark=marks['Дизлайк']).exists() is False

    def test_serializer_model(self):
        fact_model = AddRatingSerializer.Meta.model
        excepted_model = Rating
        assert fact_model == excepted_model

    def test_serializer_fields(self):
        fact_fields = set(AddRatingSerializer().fields.keys())
        expected_fields = {'mark', 'post'}
        assert fact_fields == expected_fields

    @pytest.mark.django_db
    def test_data_values_create(self, post, marks):
        post_slug = post.url
        ip = '128.0.0.1'
        data = {'mark': marks['Лайк'].id}

        serializer = AddRatingSerializer(data=data, context={'slug': post_slug})
        serializer.is_valid(raise_exception=True)
        serializer.save(ip=ip)

        fact_data_values = serializer.data
        expected_data_values = {'mark': marks['Лайк'].id, 'post': post.url}
        # Проверка №1. Совпадение ключей (полей) между ожидаемыми и фактическими данными
        assert not fact_data_values.keys() ^ expected_data_values.keys()
        # Проверка №2. У сериализатора корректные значения по каждому полю
        for field, fact_value in fact_data_values.items():
            assert fact_value == expected_data_values[field]

    @pytest.mark.django_db
    def test_data_values_update(self, post, marks):
        post_slug = post.url
        ip = '128.0.0.1'
        data = {'mark': marks['Лайк'].id}
        rating = RatingFactory(ip=ip, mark=marks['Дизлайк'], post=post)

        serializer = AddRatingSerializer(instance=rating, data=data, context={'slug': post_slug})
        serializer.is_valid(raise_exception=True)
        serializer.save(ip=ip)

        fact_data_values = serializer.data
        expected_data_values = {'mark': marks['Лайк'].id, 'post': post.url}
        # Проверка №1. Совпадение ключей (полей) между ожидаемыми и фактическими данными
        assert not fact_data_values.keys() ^ expected_data_values.keys()
        # Проверка №2. У сериализатора корректные значения по каждому полю
        for field, fact_value in fact_data_values.items():
            assert fact_value == expected_data_values[field]
