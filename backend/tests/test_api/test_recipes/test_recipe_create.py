from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import CustomUser
from tests.factories import IngredientFactory
from tests.factories import TagFactory

pytestmark = [pytest.mark.django_db]

CREATE_RECIPE_API_URL = reverse('api:recipes-list')


def test_create_recipe_api_successful(
    tag_factory: TagFactory,
    ingredient_factory: IngredientFactory,
    base64_string_image: str,
    api_user_client: tuple[CustomUser, APIClient],
) -> None:
    _, api_client = api_user_client

    tags = tag_factory.create_batch(size=3)
    ingredients = ingredient_factory.create_batch(size=4)

    payload = {
        'name': 'recipe',
        'text': 'good recipe',
        'tags': [tag.id for tag in tags],
        'ingredients': [
            {
                'id': ingredient.id,
                'amount': 50,
            }
            for ingredient in ingredients
        ],
        'cooking_time': 50,
        'image': base64_string_image,
    }
    response = api_client.post(CREATE_RECIPE_API_URL, payload, format='json')

    assert response.status_code == 201


def test_create_recipe_not_auth_user(
    tag_factory: TagFactory,
    ingredient_factory: IngredientFactory,
    base64_string_image: str,
    api_client,
) -> None:
    tags = tag_factory.create_batch(size=3)
    ingredients = ingredient_factory.create_batch(size=4)

    payload = {
        'name': 'recipe',
        'text': 'good recipe',
        'tags': [tag.id for tag in tags],
        'ingredients': [
            {
                'id': ingredient.id,
                'amount': 50,
            }
            for ingredient in ingredients
        ],
        'cooking_time': 50,
        'image': base64_string_image,
    }
    response = api_client.post(CREATE_RECIPE_API_URL, payload, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
