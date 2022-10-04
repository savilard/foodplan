import pytest
from pytest_factoryboy import register
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tests.factories.ingredient_factory import IngredientFactory
from tests.factories.recipe_factory import RecipeFactory
from tests.factories.tag_factory import TagFactory
from tests.factories.user_factory import UserFactory

register(IngredientFactory)
register(RecipeFactory)
register(UserFactory)
register(TagFactory)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_user_client(api_client: APIClient, user_factory: UserFactory) -> APIClient:
    author = user_factory.create()
    token = Token.objects.create(user=author)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client
