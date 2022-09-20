import pytest

from django.db import IntegrityError

from tests.factories.ingredient_factory import IngredientFactory

pytestmark = [pytest.mark.django_db]


def test_create_ingredient_successful(ingredient_factory: IngredientFactory) -> None:
    """Test ingredient create."""
    ingredient = ingredient_factory.create()

    assert str(ingredient) == f'{ingredient.name}, {ingredient.measurement_unit}'


def test_name_measurement_unit_unique_together(ingredient_factory: IngredientFactory) -> None:
    """Checking the uniqueness of the name and measurement unit fields together.

    Args:
        ingredient_factory: pytest ingredient factory
    """
    with pytest.raises(IntegrityError):
        ingredient_factory.create_batch(
            name='Мука',
            measurement_unit='г',
            size=2,
        )


@pytest.mark.parametrize('ingredient_name, ingredient_measurement_unit', [
    ('', 'г'),
    ('Мука', ''),
])
def test_model_check_constraint(
    ingredient_name: str,
    ingredient_measurement_unit: str,
    ingredient_factory: IngredientFactory,
) -> None:
    """Test ingredient model CheckConstraint.

    Args:
        ingredient_name: ingredient name
        ingredient_measurement_unit: measurement unit
        ingredient_factory: pytest ingredient factory
    """
    with pytest.raises(IntegrityError):
        ingredient_factory.create(
            name=ingredient_name,
            measurement_unit=ingredient_measurement_unit,
        )
