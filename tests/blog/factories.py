from django.core.files.uploadedfile import SimpleUploadedFile
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from blog.models import Category, Post, Video
from tests.users.factories import UserFactory


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


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Sequence(lambda n: f'Как я провёл отпуск. Часть {n+1}')
    url = Sequence(lambda n: f'kak-ya-provel-otpusk{n+1}')
    author = SubFactory(UserFactory)
    category = SubFactory(CategoryFactory)
    body = 'Содержание событий в отпуске'
    image = SimpleUploadedFile("fishing.jpeg", b"fake image content", content_type="image/jpeg")
