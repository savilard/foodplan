from rest_framework import serializers

from apps.recipes.api.serializers import IngredientSerializer
from apps.recipes.models import Recipe
from apps.tags.api.serializers import TagSerializer


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe model."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

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
