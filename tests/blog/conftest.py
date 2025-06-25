import pytest

from tests.blog.factories import CategoryFactory


@pytest.fixture
def category():
    return CategoryFactory()
