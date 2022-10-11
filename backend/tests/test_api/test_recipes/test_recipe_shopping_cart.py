from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import CustomUser
from tests.factories import RecipeFactory, CartFactory

pytestmark = [pytest.mark.django_db]


def get_add_recipe_to_cart_url(recipe_id: str) -> str:
    """Return a add recipe to cart url."""
    return reverse('api:recipes-shopping-cart', args=[recipe_id])


def test_add_recipe_to_cart_successful(recipe_factory: RecipeFactory, api_user_client: APIClient) -> None:
    """Test add recipe to cart is successful.

    Args:
        recipe_factory: ingredient factory;
        api_user_client: django rest framework api client.
    """
    _, api_client = api_user_client
    recipe = recipe_factory.create()

    response = api_client.post(get_add_recipe_to_cart_url(recipe_id=recipe.id))

    assert response.status_code == status.HTTP_201_CREATED


def test_add_non_existent_recipe_to_shopping_cart_error(api_user_client: APIClient) -> None:
    """Test add recipe to cart is successful.

    Args:
        api_user_client: django rest framework api client.
    """
    _, api_client = api_user_client
    non_existent_recipe_id = '999'

    response = api_client.post(get_add_recipe_to_cart_url(recipe_id=non_existent_recipe_id))

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_add_recipe_to_cart_by_an_unauthorized_user_error(recipe_factory: RecipeFactory, api_client: APIClient) -> None:
    """Test of adding a recipe to the cart by an unauthorized user.

    Args:
        recipe_factory: ingredient factory;
        api_client: django rest framework api client.
    """
    recipe = recipe_factory.create()

    response = api_client.post(get_add_recipe_to_cart_url(recipe_id=recipe.id))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_add_existing_recipe_to_shopping_cart_error(
    recipe_factory: RecipeFactory,
    cart_factory: CartFactory,
    api_user_client: tuple[CustomUser, APIClient],
) -> None:
    """Test of adding an existing recipe to the shopping cart.

    Args:
        recipe_factory: ingredient factory;
        cart_factory: shopping cart factory;
        api_user_client: django rest framework api client.
    """
    user, api_client = api_user_client

    recipes = recipe_factory.create_batch(size=2)
    cart = cart_factory.create(owner=user, recipes=recipes)

    response = api_client.post(get_add_recipe_to_cart_url(recipe_id=cart.recipes.first().id))

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_remove_recipe_from_shopping_cart_successful(
    recipe_factory: RecipeFactory,
    cart_factory: CartFactory,
    api_user_client: tuple[CustomUser, APIClient],
) -> None:
    """Test removing recipe from the shopping cart.

    Args:
        recipe_factory: ingredient factory;
        cart_factory: shopping cart factory;
        api_user_client: django rest framework api client.
    """
    user, api_client = api_user_client

    recipes = recipe_factory.create_batch(size=2)
    cart = cart_factory.create(owner=user, recipes=recipes)

    response = api_client.delete(get_add_recipe_to_cart_url(recipe_id=cart.recipes.first().id))

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_remove_non_existent_recipe_to_shopping_cart_error(api_user_client: APIClient) -> None:
    """Test removing non-existent recipe from shopping cart.

    Args:
        api_user_client: django rest framework api client.
    """
    _, api_client = api_user_client
    non_existent_recipe_id = '999'

    response = api_client.delete(get_add_recipe_to_cart_url(recipe_id=non_existent_recipe_id))

    assert response.status_code == status.HTTP_404_NOT_FOUND
