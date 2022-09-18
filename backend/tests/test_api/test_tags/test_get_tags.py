import pytest

from django.urls import reverse

from rest_framework import status

pytestmark = [pytest.mark.django_db]

GET_LISTS_URL = reverse('tags-list')
TOTAL_TAGS_NUMBER = 3


def test_get_tags_success(tag_factory, client) -> None:
    """Test getting a tags is successful.

    Args:
        tag_factory: tag factory
        client: django rest framework api client
    """
    tag_factory.create_batch(size=TOTAL_TAGS_NUMBER)
    response = client.get(GET_LISTS_URL)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == TOTAL_TAGS_NUMBER
