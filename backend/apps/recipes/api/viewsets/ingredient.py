from rest_framework import viewsets

from apps.recipes.api.serializers import IngredientSerializer
from apps.recipes.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Get a list of ingredients and ingredient by its id.

    Only admins are allowed to create and edit ingredients
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
