import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

pytestmark = [pytest.mark.django_db]

CREATE_USER_URL = reverse('api:users-list')
User = get_user_model()


def test_create_user_success(user_factory, client):
    """Test creating a user is successful.

    Args:
        user_factory: custom user factory
        client: django rest framework api client
    """
    payload = user_factory.build_payload()
    response = client.post(CREATE_USER_URL, payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert 'password' not in response.data

    user = User.objects.get(username=payload['username'])

    assert user.check_password(payload['password'])
    assert user.is_active


def test_user_with_email_exists_error(user_factory, client):
    """Test error returned if user with email exists.

    Args:
        user_factory: custom user factory
        client: django rest framework api client
    """
    user = user_factory.create(email='test@example.com')
    payload = user_factory.build_payload(user=user, user_email='test@example.com')

    response = client.post(CREATE_USER_URL, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    users_count = User.objects.count()
    assert users_count == 1


def test_user_with_wrong_email_error(user_factory, client):
    """Test error returned if user with email exists.

    Args:
        user_factory: custom user factory
        client: django rest framework api client
    """
    payload = user_factory.build_payload(user_email='wrong_email')

    response = client.post(CREATE_USER_URL, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['email'] == ['Enter a valid email address.']


def test_password_too_short_error(user_factory, client):
    """Test an error is returned if password less than 5 chars.

    Args:
        user_factory: custom user factory
        client: django rest framework api client
    """
    payload = user_factory.build_payload(user_password='123')  # noqa: S106

    response = client.post(CREATE_USER_URL, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'This password is too short. It must contain at least 8 characters.' in response.data['password']
