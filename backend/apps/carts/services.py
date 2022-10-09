from apps.carts.models import Cart
from apps.recipes.models import Recipe


def add_recipe_to(shopping_cart: Cart, recipe: Recipe):
    """Add recipe to shopping cart."""
    shopping_cart.recipes.add(recipe)


def remove_recipe_from(shopping_cart: Cart, recipe: Recipe):
    """Remove recipe from shopping cart."""
    shopping_cart.recipes.remove(recipe)
