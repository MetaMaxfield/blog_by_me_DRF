import pytest

from company.models import About
from company.serializers import AboutSerializer
from tests.company.factories import AboutFactory


class AboutSerializerTest:
    """Тестирование сериализатора AboutSerializer(ModelSerializer)"""

    def test_serializer_model(self):
        fact_model = AboutSerializer.Meta.model
        excepted_model = About
        assert fact_model == excepted_model

    def test_serializer_fields(self):
        fact_fields = set(AboutSerializer().fields.keys())
        expected_fields = {
            'id',
            'description',
            'email_contact',
            'phone1_num',
            'phone2_num',
            'address',
            'latitude',
            'longitude',
        }
        assert fact_fields == expected_fields

    @pytest.mark.django_db
    def test_serializer_data_values(self):
        expected_data_values = {
            'id': 1,
            'description': 'Описание компании',
            'email_contact': 'testmail@gmail.com',
            'phone1_num': '+79999999999',
            'phone2_num': '+79998888888',
            'address': 'Адрес компании',
            'latitude': '51.532065',
            'longitude': '46.032558',
        }
        about = AboutFactory(**expected_data_values)
        fact_data_values = AboutSerializer(about).data

        for field, fact_value in fact_data_values.items():
            assert fact_value == expected_data_values[field]
