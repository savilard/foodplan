from django.db import transaction

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.recipes.api.pagination import LimitPageNumberPagination
from apps.recipes.api.permissions import IsOwnerOrReadOnly
from apps.recipes.api.serializers import RecipeSerializer
from apps.recipes.api.serializers.recipe import RecipeCreateSerializer
from apps.recipes.api.validators.recipe import validate_recipe_data
from apps.recipes.models import Recipe
from apps.recipes.services import RecipeService


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('tags', 'ingredients')
    recipe_retrieve_serializer_class = RecipeSerializer
    recipe_create_serializer_class = RecipeCreateSerializer
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        validated_data = validate_recipe_data(recipe_data=request.data, serializer=self.recipe_create_serializer_class)
        service = RecipeService(author=self.request.user, validated_data=validated_data)
        recipe = service.create()
        return Response(self.recipe_retrieve_serializer_class(recipe).data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action in {'create', 'update', 'partial_update'}:
            return self.recipe_create_serializer_class
        return self.recipe_retrieve_serializer_class
