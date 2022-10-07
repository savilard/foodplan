from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories import RecipeFactory

pytestmark = [pytest.mark.django_db]

GET_RECIPE_LIST_URL = reverse('api:recipes-list')
TOTAL_RECIPES_NUMBER = 3


def test_get_recipes_success(recipe_factory: RecipeFactory, api_user_client: APIClient) -> None:
    """Test getting recipes is successful.

    Args:
        recipe_factory: recipe factory
        api_user_client: django rest framework api client
    """
    recipe_factory.create_batch(size=TOTAL_RECIPES_NUMBER)
    response = api_user_client.get(GET_RECIPE_LIST_URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['count'] == TOTAL_RECIPES_NUMBER
