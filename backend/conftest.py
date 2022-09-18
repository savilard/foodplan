from pytest_factoryboy import register

from tests.factories.tag_factory import TagFactory
from tests.factories.user_factory import UserFactory

register(UserFactory)
register(TagFactory)
