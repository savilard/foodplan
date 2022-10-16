import typing

from django.db import transaction

from rest_framework.generics import get_object_or_404

from apps.recipes.models import Recipe
from apps.recipes.models.recipes import RecipeIngredient
from apps.users.models import CustomUser


class RecipeService(object):
    """Service for creating recipe."""

    def __init__(self, author: CustomUser | typing.Any, validated_data) -> None:
        """Init for RecipeService.

        Args:
            author: recipe author, authorized user
            validated_data: validated recipe data from the frontend.
        """
        self.author: CustomUser = author
        self.validated_data = validated_data

    @transaction.atomic
    def create(self) -> Recipe:
        """Create recipe."""
        ingredients = self.validated_data.pop('recipe_ingredients')
        tags = self.validated_data.pop('tags')

        recipe = Recipe.objects.create(author=self.author, **self.validated_data)
        recipe.tags.set(tags)
        self._add_ingredients_to(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self) -> Recipe:
        """Update recipe."""
        recipe_id = self.validated_data.pop('id')
        tags = self.validated_data.pop('tags')
        ingredients = self.validated_data.pop('recipe_ingredients')

        recipe = get_object_or_404(Recipe, id=recipe_id)

        recipe.name = self.validated_data.get('name')
        recipe.text = self.validated_data.get('text')
        recipe.cooking_time = self.validated_data.get('cooking_time')

        recipe.save()

        recipe.tags.set(tags)

        RecipeIngredient.objects.filter(recipe=recipe).delete()
        self._add_ingredients_to(recipe, ingredients)

        recipe.refresh_from_db()

        return recipe

    @staticmethod
    def _add_ingredients_to(recipe: Recipe, ingredients):
        """Add ingredients to recipe.

        Args:
            recipe: a recipe in which you need to add ingredients;
            ingredients: recipe ingredients
        """
        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient.get('ingredient'),
                    amount=ingredient.get('amount'),
                )
                for ingredient in ingredients
            ],
        )
