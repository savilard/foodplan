import pytest
from uuid import UUID

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from tests.factories import TagFactory

pytestmark = [pytest.mark.django_db]


def get_tag_detail_url(tag_id: str) -> str:
    """Return a tag detail url."""
    return reverse('api:tags-detail', args=[tag_id])


def test_retrieve_tag_success(tag_factory: TagFactory, client: APIClient) -> None:
    """Test retrieve tag is successful.

    Args:
        tag_factory: tag factory;
        client: django rest framework api client.
    """
    tag = tag_factory.create()

    response = client.get(get_tag_detail_url(tag_id=tag.id))

    assert response.status_code == status.HTTP_200_OK
    assert UUID(response.json()['id']) == tag.id


def test_retrieve_tag_non_existent_error(client: APIClient) -> None:
    """Test retrieve non existent tag.

    Args:
        client: django rest framework api client.
    """
    incorrect_tag_id = '69cb997c-aaa4-4c30-8112-1623814418e8'

    response = client.get(get_tag_detail_url(tag_id=incorrect_tag_id))

    assert response.status_code == status.HTTP_404_NOT_FOUND
