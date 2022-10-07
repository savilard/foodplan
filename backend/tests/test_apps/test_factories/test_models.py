from django.db import IntegrityError

import pytest

from tests.factories import FavoritesFactory
from tests.factories import RecipeFactory
from tests.factories import UserFactory

pytestmark = [pytest.mark.django_db]


def test_create_favorites(favorites_factory: FavoritesFactory) -> None:
    """Test favorites create."""
    favorites = favorites_factory.create()

    assert str(favorites.user.username) == favorites.user.username


def test_user_recipe_unique_together(
    user_factory: UserFactory,
    recipe_factory: RecipeFactory,
    favorites_factory: FavoritesFactory,
) -> None:
    """Checking the uniqueness of the user and recipe fields together.

    Args:
        favorites_factory: pytest favorites factory
    """
    user = user_factory.create()
    recipe = recipe_factory.create()
    with pytest.raises(IntegrityError):
        favorites_factory.create_batch(
            user=user,
            recipe=recipe,
            size=2,
        )
