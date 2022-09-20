from factory.django import DjangoModelFactory

from apps.recipes.models import Ingredient
from tests.factories.mixins import UniqueStringMixin


class IngredientFactory(DjangoModelFactory):
    """Ingredient factory."""

    name = UniqueStringMixin('word')
    measurement_unit = UniqueStringMixin('word')

    class Meta:
        model = Ingredient
