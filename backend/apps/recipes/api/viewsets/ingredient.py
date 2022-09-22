from rest_framework import viewsets

from django_filters import rest_framework as filters

from apps.recipes.api.filters.ingredients import IngredientFilterSet
from apps.recipes.api.serializers import IngredientSerializer
from apps.recipes.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Get a list of ingredients and ingredient by its id.

    Only admins are allowed to create and edit ingredients
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilterSet
