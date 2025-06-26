import pytest

from tests.blog.factories import CategoryFactory, PostFactory, VideoFactory


@pytest.fixture
def category():
    return CategoryFactory()


@pytest.fixture
def video():
    return VideoFactory()


@pytest.fixture
def post():
    return PostFactory()
