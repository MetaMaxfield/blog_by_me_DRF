from factory import Faker
from factory.django import DjangoModelFactory

from company.models import About


class AboutFactory(DjangoModelFactory):
    class Meta:
        model = About

    description = 'Описание компании'
    email_contact = Faker('email')
    phone1_num = Faker('phone_number')
    phone2_num = Faker('phone_number')
    address = 'Адрес компании'
    latitude = '51.532065'
    longitude = '46.032558'
