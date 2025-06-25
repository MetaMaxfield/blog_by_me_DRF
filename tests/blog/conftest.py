import pytest

from tests.blog.factories import CategoryFactory, VideoFactory


@pytest.fixture
def category():
    return CategoryFactory()


@pytest.fixture
def video():
    return VideoFactory()
