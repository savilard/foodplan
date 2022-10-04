from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from apps.recipes.api.serializers import IngredientSerializer
from apps.recipes.models import Ingredient
from apps.recipes.models import Recipe
from apps.recipes.models.recipes import RecipeIngredient
from apps.tags.api.serializers import TagSerializer
from apps.tags.models import Tag
from apps.users.api.serializers import CustomUserCreateSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
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


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    author = CustomUserCreateSerializer(read_only=True)

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
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Serializer for create recipe."""

    image = Base64ImageField()
    ingredients = RecipeIngredientSerializer(
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
