import pytest

from tests.factories import RecipeFactory
from tests.factories import UserFactory

pytestmark = [pytest.mark.django_db]


def test_create_recipe_successful(recipe_factory: RecipeFactory, user_factory: UserFactory) -> None:
    author = user_factory.create()
    recipe = recipe_factory.create(author=author)

    assert recipe.author.id == author.id
    assert len(recipe.ingredients.all()) > 0
    assert len(recipe.tags.all()) > 0
    assert str(recipe) == recipe.name
