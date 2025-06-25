from django.core.files.uploadedfile import SimpleUploadedFile
from factory import Sequence
from factory.django import DjangoModelFactory

from blog.models import Category, Video


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Sequence(lambda n: f'Категория {n+1}')
    description = 'Описание категории'
    url = Sequence(lambda n: f'category{n+1}')


class VideoFactory(DjangoModelFactory):
    class Meta:
        model = Video

    title = 'Рыбалка'
    description = 'Видео с большим уловом'
    file = SimpleUploadedFile("fishing.mp4", b"fake video content", content_type="video/mp4")
