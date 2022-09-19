import pytest

from django.db import IntegrityError

from tests.factories.tag_factory import TagFactory

pytestmark = [pytest.mark.django_db]


def test_name_color_unique_together(tag_factory: TagFactory) -> None:
    """Checking the uniqueness of the name and color fields together.

    Args:
        tag_factory: pytest tag factory
    """
    with pytest.raises(IntegrityError):
        tag_factory.create_batch(
            name='Завтрак',
            color='#55A15E',
            slug='breakfast',
            size=2,
        )


@pytest.mark.parametrize('tag_name, tag_color, tag_slug', [
    ('', '#55A15E', 'breakfast'),
    ('Завтрак', '#55A15E', ''),
    ('Обед', '55A15E', 'lunch'),
    ('Ужин', '#', 'dinner'),
    ('Перекус', '#5', 'snack-time'),
    ('Полдник', '#55', 'afternoon-snack'),
])
def test_model_check_constraint(tag_name: str, tag_color: str, tag_slug: str, tag_factory: TagFactory) -> None:
    """Test tag model CheckConstraint.

    Args:
        tag_name: tag name
        tag_color: tag color
        tag_slug: tag slug
        tag_factory: pytest tag factory
    """
    with pytest.raises(IntegrityError):
        tag_factory.create(
            name=tag_name,
            color=tag_color,
            slug=tag_slug,
        )
