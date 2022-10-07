from uuid import UUID

from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories import RecipeFactory

pytestmark = [pytest.mark.django_db]


def get_recipe_detail_url(recipe_id: str) -> str:
    """Return a recipe detail url."""
    return reverse('api:recipes-detail', args=[recipe_id])


def test_retrieve_recipe_success(recipe_factory: RecipeFactory, api_user_client: APIClient) -> None:
    """Test retrieve recipe is successful.

    Args:
        recipe_factory: ingredient factory;
        api_user_client: django rest framework api client.
    """
    recipe = recipe_factory.create()

    response = api_user_client.get(get_recipe_detail_url(recipe_id=recipe.id))

    assert response.status_code == status.HTTP_200_OK
    assert UUID(response.json()['id']) == recipe.id


def test_retrieve_recipe_non_existent_error(api_client: APIClient) -> None:
    """Test retrieve non existent recipe.

    Args:
        api_client: django rest framework api client.
    """
    incorrect_recipe_id = '69cb997c-aaa4-4c30-8112-1623814418e8'

    response = api_client.get(get_recipe_detail_url(recipe_id=incorrect_recipe_id))

    assert response.status_code == status.HTTP_404_NOT_FOUND
