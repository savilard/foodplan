from pytest_factoryboy import register

from tests.factories.ingredient_factory import IngredientFactory
from tests.factories.tag_factory import TagFactory
from tests.factories.user_factory import UserFactory

register(IngredientFactory)
register(UserFactory)
register(TagFactory)
