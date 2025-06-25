from factory import Sequence
from factory.django import DjangoModelFactory

from users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f'Maximus{n + 1}')
    description = 'Описание пользователя'
    email = Sequence(lambda n: f'maximus{n + 1}@gmail.com')
