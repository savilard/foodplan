from django.db import models

from apps.carts.models import Cart
from apps.favorites.models import Favorites
from apps.users.models import CustomUser


class RecipeQuerySet(models.QuerySet):
    """Recipe model custom queryset."""

    def with_favorites_status(self, user: CustomUser) -> 'models.QuerySet':
        """Returns recipes with the status of adding the recipe to favorites for the transferred user."""
        favorites = Favorites.objects.filter(
            recipe=models.OuterRef('id'),
        )
        return self.annotate(
            is_favorited=models.Exists(
                favorites.filter(user=user),
            ),
        )

    def with_is_in_shopping_cart_status(self, user: CustomUser) -> 'models.QuerySet':
        """Returns recipes with the status of adding to the shopping list for the transferred user."""
        user_cart = Cart.objects.filter(
            owner=user,
            recipes=models.OuterRef('pk'),
        )
        return self.annotate(
            is_in_shopping_cart=models.Exists(user_cart),
        )
