from unittest import mock

import pytest
from rest_framework.test import APIClient

from blog_by_me_DRF.settings import KEY_AUTHOR_DETAIL, KEY_AUTHORS_LIST
from users.serializers import AuthorDetailSerializer, AuthorListSerializer


class AuthorViewSetTest:
    """Тестирование представления AuthorViewSet(ReadOnlyModelViewSet)"""

    def _make_request_list(self):
        return APIClient().get('/api/v1/authors/')

    def _make_request_retrieve(self, user_id):
        return APIClient().get(f'/api/v1/authors/{user_id}/')

    @pytest.mark.django_db
    def test_view_list_url(self):
        response = self._make_request_list()
        fact_status_code = response.status_code
        expected_status_code = 200
        assert fact_status_code == expected_status_code

    @pytest.mark.django_db
    def test_view_retrieve_url(self, user):
        response = self._make_request_retrieve(user.id)
        fact_status_code = response.status_code
        expected_status_code = 200
        assert fact_status_code == expected_status_code

    @pytest.mark.django_db
    def test_view_retrieve_not_found(self):
        not_exist_user_id = 999
        response = self._make_request_retrieve(not_exist_user_id)
        fact_status_code = response.status_code
        expected_status_code = 404
        assert fact_status_code == expected_status_code

    @mock.patch('users.views.AuthorListSerializer')
    @mock.patch('users.views.AuthorViewSet.get_queryset')
    def test_view_list_get_serializer_class(self, mock_queryset, mock_serializer):
        mock_queryset.return_value = [mock.Mock(), mock.Mock()]
        mock_serializer.return_value = mock.Mock(data=[])
        _ = self._make_request_list()
        mock_serializer.assert_called_once()

    @mock.patch('users.views.AuthorDetailSerializer')
    @mock.patch('users.views.AuthorViewSet.get_object')
    def test_view_retrieve_get_serializer_class(self, mock_object, mock_serializer):
        test_user_id = 1
        mock_object.return_value = mock.Mock(id=test_user_id)
        mock_serializer.return_value = mock.Mock(data=[])
        _ = APIClient().get(f'/api/v1/authors/{test_user_id}/')
        mock_serializer.assert_called_once()

    @mock.patch('users.views.get_cached_objects_or_queryset')
    def test_view_list_get_queryset_return_mock(self, mock_get_cached_objects_or_queryset):
        _ = self._make_request_list()
        mock_get_cached_objects_or_queryset.assert_called_once_with(KEY_AUTHORS_LIST)

    @pytest.mark.django_db
    def test_view_list_get_queryset_return_not_mock(self, users):
        response = self._make_request_list()
        fact_data = response.data
        expected_data = AuthorListSerializer(users, many=True).data
        assert fact_data == expected_data

    @pytest.mark.django_db
    @mock.patch('users.views.get_cached_objects_or_queryset')
    def test_view_retrieve_get_queryset_return_mock(self, mock_get_cached_objects_or_queryset, user):
        mock_get_cached_objects_or_queryset.return_value = user
        _ = self._make_request_retrieve(user.id)
        mock_get_cached_objects_or_queryset.assert_called_once_with(KEY_AUTHOR_DETAIL, pk=str(user.id))

    @pytest.mark.django_db
    def test_view_retrieve_get_queryset_return_not_mock(self, user):
        response = self._make_request_retrieve(user.id)
        fact_data = response.data
        expected_data = AuthorDetailSerializer(user, many=False).data
        assert fact_data == expected_data
