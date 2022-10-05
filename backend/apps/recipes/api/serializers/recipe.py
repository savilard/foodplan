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
    author = CustomUserSerializer(read_only=True)

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


class CropRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


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

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return user.followers.filter(id=obj.id).exists()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj)
        if limit:
            queryset = queryset[:int(limit)]
        return CropRecipeSerializer(queryset, many=True).data
