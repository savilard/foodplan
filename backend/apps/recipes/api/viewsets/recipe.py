from django.db import transaction

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.recipes.api.pagination import LimitPageNumberPagination
from apps.recipes.api.permissions import IsOwnerOrReadOnly
from apps.recipes.api.serializers import RecipeRetrieveSerializer
from apps.recipes.api.serializers.recipe import RecipeCreateSerializer, RecipeUpdateSerializer
from apps.recipes.api.validators.recipe import validate_recipe_data
from apps.recipes.models import Recipe
from apps.recipes.services import RecipeService


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('tags', 'ingredients')
    recipe_retrieve_serializer_class = RecipeRetrieveSerializer
    recipe_create_serializer_class = RecipeCreateSerializer
    recipe_update_serializer_class = RecipeUpdateSerializer
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        validated_data = validate_recipe_data(recipe_data=request.data, serializer=self.recipe_create_serializer_class)
        service = RecipeService(author=self.request.user, validated_data=validated_data)
        recipe = service.create()
        return Response(
            self.recipe_retrieve_serializer_class(recipe, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, *args, **kwargs):
        validated_data = validate_recipe_data(recipe_data=request.data, serializer=self.recipe_update_serializer_class)
        service = RecipeService(author=self.request.user, validated_data=validated_data)
        recipe = service.update()

        return Response(
            self.recipe_retrieve_serializer_class(recipe, context={'request': request}).data,
            status=status.HTTP_200_OK,
        )

    def get_serializer_class(self):
        if self.action in {'create', 'update', 'partial_update'}:
            return self.recipe_create_serializer_class
        return self.recipe_retrieve_serializer_class
