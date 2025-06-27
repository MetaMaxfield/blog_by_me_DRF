import pytest

from services import queryset
from tests.users.factories import UserFactory


@pytest.fixture
def users():
    UserFactory.create_batch(3)
    return queryset._qs_author_list()
