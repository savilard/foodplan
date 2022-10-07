import typing

from django.db import transaction
from django.http import HttpRequest
from django.http import HttpResponse

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.favorites.models import Favorites
from apps.recipes.api.pagination import LimitPageNumberPagination
from apps.recipes.api.permissions import IsOwnerOrReadOnly
from apps.recipes.api.serializers import RecipeRetrieveSerializer
from apps.recipes.api.serializers.recipe import RecipeCreateSerializer, RecipeUpdateSerializer, CropRecipeSerializer
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

    @action(methods=['post'], detail=True, permission_classes=(IsAuthenticated,))
    def favorite(self, request: HttpRequest, pk: typing.Optional[str] = None) -> HttpResponse:  # noqa: WPS125
        """Add recipe to favorites.

        Args:
            request: drf request;
            pk: recipe id.
        """
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorites, created = Favorites.objects.get_or_create(user=user, recipe=recipe)
        if not created:
            return Response(
                {'errors': 'The recipe has already been added to favorites'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            CropRecipeSerializer(recipe, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    @favorite.mapping.delete
    def remove_recipe_from_favorite(self, request: HttpRequest, pk: typing.Optional[str] = None) -> HttpResponse:  # noqa: WPS125
        """Remove recipe from favorites.

        Args:
            request: drf request;
            pk: recipe id.
        """
        user = request.user
        if user.is_anonymous:
            return Response(
                {'errors': 'The user is not authorized.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        recipe = get_object_or_404(Recipe, id=pk)
        favorites = Favorites.objects.filter(user=user, recipe=recipe)
        if not favorites.first():
            return Response(
                {'errors': 'The recipe you requested has not been added to favorites.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_deleted, _ = favorites.delete()
        if not is_deleted:
            return Response(
                {
                    'errors': 'The recipe was not in the favorites.',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action in {'create', 'update', 'partial_update'}:
            return self.recipe_create_serializer_class
        return self.recipe_retrieve_serializer_class
