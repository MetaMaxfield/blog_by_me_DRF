from factory import Sequence
from factory.django import DjangoModelFactory

from blog.models import Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Sequence(lambda n: f'Категория {n+1}')
    description = 'Описание категории'
    url = Sequence(lambda n: f'category{n+1}')
