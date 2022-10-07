from uuid import UUID

from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories import IngredientFactory

pytestmark = [pytest.mark.django_db]


def get_ingredient_detail_url(ingredient_id: str) -> str:
    """Return a ingredient detail url."""
    return reverse('api:ingredients-detail', args=[ingredient_id])


def test_retrieve_ingredient_success(ingredient_factory: IngredientFactory, client: APIClient) -> None:
    """Test retrieve ingredient is successful.

    Args:
        ingredient_factory: ingredient factory;
        client: django rest framework api client.
    """
    ingredient = ingredient_factory.create()

    response = client.get(get_ingredient_detail_url(ingredient_id=ingredient.id))

    assert response.status_code == status.HTTP_200_OK
    assert UUID(response.json()['id']) == ingredient.id


def test_retrieve_ingredient_non_existent_error(client: APIClient) -> None:
    """Test retrieve non existent ingredient.

    Args:
        client: django rest framework api client.
    """
    incorrect_tag_id = '69cb997c-aaa4-4c30-8112-1623814418e8'

    response = client.get(get_ingredient_detail_url(ingredient_id=incorrect_tag_id))

    assert response.status_code == status.HTTP_404_NOT_FOUND
