import typing

from django.db.models import QuerySet

from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from apps.carts.models import Cart
from apps.favorites.models import Favorites
from apps.recipes.api import serializers as recipe_serializers
from apps.recipes.api.filters.recipe import RecipeFilter
from apps.recipes.api.pagination import LimitPageNumberPagination
from apps.recipes.api.permissions import IsOwnerOrReadOnly
from apps.recipes.api.validators.recipe import validate_recipe_data
from apps.recipes.models import Recipe
from apps.recipes.selectors.recipe import get_recipes_for
from apps.recipes.services import RecipeService


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('tags', 'recipe_ingredients__ingredient')

    recipe_retrieve_serializer_class = recipe_serializers.RecipeRetrieveSerializer
    recipe_create_serializer_class = recipe_serializers.RecipeCreateSerializer
    recipe_update_serializer_class = recipe_serializers.RecipeUpdateSerializer

    pagination_class = LimitPageNumberPagination

    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

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
    def favorite(self, request: Request, pk: typing.Optional[str] = None) -> Response:  # noqa: WPS125
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
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            recipe_serializers.CropRecipeSerializer(recipe, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    @favorite.mapping.delete
    def remove_recipe_from_favorite(self, request: Request,
                                    pk: typing.Optional[str] = None) -> Response:  # noqa: WPS125
        """Remove recipe from favorites.

        Args:
            request: drf request;
            pk: recipe id.
        """
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorites = Favorites.objects.filter(user=user, recipe=recipe)  # type: ignore
        if not favorites.first():
            return Response(
                {'errors': 'The recipe you requested has not been added to favorites.'},
                status=status.HTTP_400_BAD_REQUEST,
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

    @action(methods=['post'], detail=True, permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request: Request, pk: typing.Optional[str] = None) -> Response:  # noqa: WPS125
        """Add recipe to shopping cart.

        Args:
            request: drf request;
            pk: recipe id.
        """
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        cart, _ = Cart.objects.prefetch_related('recipes').get_or_create(owner=user)

        if recipe.id in cart.recipes.values_list('id', flat=True):
            return Response(
                {'errors': 'The recipe has already been added to favorites'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart.recipes.add(recipe)

        return Response(
            recipe_serializers.CropRecipeSerializer(recipe, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    def get_serializer_class(self):
        if self.action in {'create', 'update', 'partial_update'}:
            return self.recipe_create_serializer_class
        return self.recipe_retrieve_serializer_class

    def get_queryset(self) -> 'QuerySet[Recipe]':
        current_user = self.request.user
        queryset = self.queryset
        if current_user.is_anonymous:
            return queryset
        return get_recipes_for(current_user, queryset=queryset)
