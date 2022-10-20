import pytest

from tests.factories import UserFactory

pytestmark = [pytest.mark.django_db]


def test_create_tag(user_factory: UserFactory) -> None:
    """Test tag create."""
    user = user_factory.create()

    assert str(user) == user.username
