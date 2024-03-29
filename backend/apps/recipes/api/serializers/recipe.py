from collections import OrderedDict
import typing

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from apps.recipes.api.serializers import IngredientSerializer
from apps.recipes.models import Ingredient
from apps.recipes.models import Recipe
from apps.recipes.models.recipes import RecipeIngredient
from apps.tags.api.serializers import TagSerializer
from apps.tags.models import Tag
from apps.users.api.serializers import CustomUserSerializer
from apps.users.models import CustomUser
from apps.users.selectors import is_user_subscribed_to_author


class RecipeIngredientRetrieveSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = (
            'ingredient',
            'amount',
        )

    def to_representation(self, instance: RecipeIngredient) -> OrderedDict:
        """Return ingredient values in one dictionary."""
        representation = super().to_representation(instance)

        ingredient_representation = representation.pop('ingredient')
        for key in ingredient_representation.keys():
            representation[key] = ingredient_representation[key]

        return representation


class RecipeRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientRetrieveSerializer(
        source='recipe_ingredients',
        many=True,
    )
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'text',
            'image',
            'ingredients',
            'tags',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, recipe: Recipe) -> typing.Optional[bool]:
        """Checks if a recipe has been added to favorites."""
        if hasattr(recipe, 'is_favorited'):  # noqa: WPS421
            return recipe.is_favorited
        return None

    def get_is_in_shopping_cart(self, recipe: Recipe) -> typing.Optional[bool]:
        """Checks if a recipe has been added to shopping cart."""
        if hasattr(recipe, 'is_in_shopping_cart'):  # noqa: WPS421
            return recipe.is_in_shopping_cart
        return None


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Serializer for create recipe."""

    image = Base64ImageField()
    ingredients = RecipeIngredientCreateSerializer(
        many=True,
        source='recipe_ingredients',
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'name',
            'text',
            'image',
            'ingredients',
            'tags',
            'cooking_time',
        )


class CropRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class RecipeUpdateSerializer(serializers.ModelSerializer):
    """Serializer for update recipe."""

    ingredients = RecipeIngredientCreateSerializer(
        many=True,
        source='recipe_ingredients',
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    id = serializers.CharField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
        )


class RecipeAuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes_count',
            'recipes',
        )
        read_only_fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes_count',
            'recipes',
        )

    def get_is_subscribed(self, recipe_author):
        """Checks if the user is subscribed to the author of the recipe.

        Args:
            recipe_author: recipe author.
        """
        user = self.context['request'].user
        return is_user_subscribed_to_author(user=user, author=recipe_author)

    def get_recipes_count(self, recipe_author):
        """Get number of recipes by the author.

        Args:
            recipe_author: recipe author
        """
        return Recipe.objects.filter(author=recipe_author).count()

    def get_recipes(self, recipe_author):
        """Get recipes by the author.

        Args:
            recipe_author: recipe author
        """
        request = self.context.get('request')
        if not request:
            return None
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=recipe_author)
        if limit:
            queryset = queryset[:int(limit)]
        return CropRecipeSerializer(queryset, many=True).data
