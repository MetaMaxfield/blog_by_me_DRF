from datetime import timedelta
from unittest import mock

import pytest
from django.core.management import call_command
from django.utils import timezone

from blog.models import Mark
from services import queryset
from tests.blog.factories import CategoryFactory, PostFactory, VideoFactory
from tests.users.factories import UserFactory


@pytest.fixture
def category():
    return CategoryFactory()


@pytest.fixture
def video():
    return VideoFactory()


@pytest.fixture
def post():
    return PostFactory()


@pytest.fixture
def filtered_posts_and_timezone_now():
    time_now = timezone.now()

    user = UserFactory()
    category = CategoryFactory()

    # Создание двух ожидаемых постов
    PostFactory.create_batch(2, author=user, category=category, publish=time_now, draft=False)

    # Создание постов не проходящих фильтрацию
    PostFactory.create(author=user, category=category, publish=time_now, draft=True)  # Пост-черновик
    PostFactory.create(author=user, category=category, publish=time_now + timedelta(seconds=30))  # Неопубликованный

    # Мок для использования единого времени в запросах фикстуры и в запросах тестов (publish__lte=timezone.now())
    with mock.patch('services.queryset.timezone.now') as mock_timezone:
        mock_timezone.return_value = time_now
        filtered_posts = queryset._qs_simple_post_list()

    return {'filtered_posts': filtered_posts, 'time_now': time_now}


@pytest.fixture
def marks():
    call_command('create_mark_models')
    return {'Лайк': Mark.objects.get(nomination='Лайк'), 'Дизлайк': Mark.objects.get(nomination='Дизлайк')}
