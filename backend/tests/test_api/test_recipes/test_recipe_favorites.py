from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import CustomUser
from tests.factories import RecipeFactory, CartFactory, FavoritesFactory

pytestmark = [pytest.mark.django_db]


def get_add_recipe_to_favorites_url(recipe_id: str) -> str:
    """Return a add recipe to favorites url."""
    return reverse('api:recipes-favorite', args=[recipe_id])


def test_add_recipe_to_favorites_successful(recipe_factory: RecipeFactory, api_user_client: APIClient) -> None:
    """Test add recipe to cart is successful.

    Args:
        recipe_factory: ingredient factory;
        api_user_client: django rest framework api client.
    """
    _, api_client = api_user_client
    recipe = recipe_factory.create()

    response = api_client.post(get_add_recipe_to_favorites_url(recipe_id=recipe.id))

    assert response.status_code == status.HTTP_201_CREATED


def test_add_existing_recipe_to_favorites_error(
    recipe_factory: RecipeFactory,
    favorites_factory: FavoritesFactory,
    api_user_client: tuple[CustomUser, APIClient],
) -> None:
    """Test of adding an existing recipe to the favorites.

    Args:
        recipe_factory: ingredient factory;
        favorites_factory: favorites factory;
        api_user_client: django rest framework api client.
    """
    user, api_client = api_user_client

    recipe = recipe_factory.create()
    favorites = favorites_factory.create(user=user, recipe=recipe)

    response = api_client.post(get_add_recipe_to_favorites_url(recipe_id=favorites.recipe.id))

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_remove_recipe_from_favorites_successful(
    recipe_factory: RecipeFactory,
    favorites_factory: FavoritesFactory,
    api_user_client: tuple[CustomUser, APIClient],
) -> None:
    """Test removing recipe from the favorites.

    Args:
        recipe_factory: ingredient factory;
        favorites_factory: favorites factory;
        api_user_client: django rest framework api client.
    """
    user, api_client = api_user_client

    recipe = recipe_factory.create()
    favorites = favorites_factory.create(user=user, recipe=recipe)

    response = api_client.delete(get_add_recipe_to_favorites_url(recipe_id=favorites.recipe.id))

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_remove_non_existent_recipe_form_favorites_error(api_user_client: APIClient) -> None:
    """Test removing non-existent recipe from favorites.

    Args:
        api_user_client: django rest framework api client.
    """
    _, api_client = api_user_client
    non_existent_recipe_id = '999'

    response = api_client.delete(get_add_recipe_to_favorites_url(recipe_id=non_existent_recipe_id))

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_remove_recipe_from_favorites_error(
    api_user_client: APIClient,
    recipe_factory: RecipeFactory,
) -> None:
    """Test removing non-existent recipe from shopping cart.

    Args:
        api_user_client: django rest framework api client.
    """
    _, api_client = api_user_client
    recipe = recipe_factory.create()

    response = api_client.delete(get_add_recipe_to_favorites_url(recipe_id=recipe.id))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
