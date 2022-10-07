from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories import IngredientFactory

pytestmark = [pytest.mark.django_db]

GET_INGREDIENT_LIST_URL = reverse('api:ingredients-list')
TOTAL_INGREDIENTS_NUMBER = 3


def test_get_ingredients_success(ingredient_factory: IngredientFactory, client: APIClient) -> None:
    """Test getting ingredients is successful.

    Args:
        ingredient_factory: tag factory
        client: django rest framework api client
    """
    ingredient_factory.create_batch(size=TOTAL_INGREDIENTS_NUMBER)
    response = client.get(GET_INGREDIENT_LIST_URL)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == TOTAL_INGREDIENTS_NUMBER
