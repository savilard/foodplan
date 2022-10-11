from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories import RecipeFactory

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
    recipe = recipe_factory.create()

    response = api_user_client.post(get_add_recipe_to_cart_url(recipe_id=recipe.id))

    assert response.status_code == status.HTTP_201_CREATED


def test_add_recipe_to_cart_by_an_unauthorized_user_error(recipe_factory: RecipeFactory, api_client: APIClient) -> None:
    """Test of adding a recipe to the cart by an unauthorized user.

    Args:
        recipe_factory: ingredient factory;
        api_client: django rest framework api client.
    """
    recipe = recipe_factory.create()

    response = api_client.post(get_add_recipe_to_cart_url(recipe_id=recipe.id))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
