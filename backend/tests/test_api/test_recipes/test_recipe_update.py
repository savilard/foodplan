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


def test_update_recipe_successful(recipe_factory: RecipeFactory, api_user_client: APIClient) -> None:
    """Test retrieve recipe is successful.

    Args:
        recipe_factory: ingredient factory;
        api_user_client: django rest framework api client.
    """
    user, api_client = api_user_client
    recipe = recipe_factory.create(author=user)

    payload = {
        'id': recipe.id,
        'name': 'recipe',
        'text': 'good recipe',
        'tags': [tag.id for tag in recipe.tags.all()],
        'ingredients': [
            {
                'id': ingredient.id,
                'amount': 50,
            }
            for ingredient in recipe.ingredients.all()
        ],
        'cooking_time': 50,
    }

    response = api_client.patch(get_recipe_detail_url(recipe_id=recipe.id), payload, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'recipe'
