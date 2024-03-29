from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import CustomUser
from tests.factories import UserFactory

pytestmark = [pytest.mark.django_db]


def get_user_subscription_url_to(recipe_author_id: str) -> str:
    return reverse('api:users-subscribe', args=[recipe_author_id])


def get_user_subscriptions_url():
    return reverse('api:users-subscriptions')


def test_subscribe_auth_user_to_recipe_author_successful(
    user_factory: UserFactory,
    api_user_client: tuple[CustomUser, APIClient],
) -> None:
    user, api_client = api_user_client

    recipe_author = user_factory.create()

    response = api_client.post(
        get_user_subscription_url_to(recipe_author.id),
        recipe_author.id,
        format='json',
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert user.follow_by.filter(id=recipe_author.id).exists()


def test_user_self_subscription_error(api_user_client: tuple[CustomUser, APIClient]) -> None:
    user, api_client = api_user_client

    response = api_client.post(
        get_user_subscription_url_to(user.id),
        user.id,
        format='json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['errors'] == 'You cannot subscribe to yourself'


def test_user_already_subscription_to_recipe_author_error(
    user_factory: UserFactory,
    api_user_client: tuple[CustomUser, APIClient],
) -> None:
    user, api_client = api_user_client

    recipe_author = user_factory.create()
    user.follow_by.add(recipe_author)

    response = api_client.post(
        get_user_subscription_url_to(recipe_author.id),
        recipe_author.id,
        format='json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['errors'] == 'You are already subscribed to this user'


def test_unsubscribe_auth_user_from_recipe_author_successful(
    user_factory: UserFactory,
    api_user_client: tuple[CustomUser, APIClient],
) -> None:
    user, api_client = api_user_client

    recipe_author = user_factory.create()
    user.follow_by.add(recipe_author)

    response = api_client.delete(
        get_user_subscription_url_to(recipe_author.id),
        recipe_author.id,
        format='json',
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_unsubscribe_non_auth_user_from_recipe_author_error(
    user_factory: UserFactory,
    user: CustomUser,
    api_client: APIClient,
) -> None:
    recipe_author = user_factory.create()
    user.follow_by.add(recipe_author)

    response = api_client.delete(
        get_user_subscription_url_to(recipe_author.id),
        recipe_author.id,
        format='json',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_self_unsubscription_error(api_user_client: tuple[CustomUser, APIClient]) -> None:
    user, api_client = api_user_client

    response = api_client.delete(
        get_user_subscription_url_to(user.id),
        user.id,
        format='json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_user_subscriptions_successful(
    api_user_client: tuple[CustomUser, APIClient],
    user_factory: UserFactory,
) -> None:
    user, api_client = api_user_client

    recipe_author = user_factory.create()
    user.follow_by.add(recipe_author)

    response = api_client.get(get_user_subscriptions_url())

    assert response.status_code == status.HTTP_200_OK
