import typing

from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet

from apps.carts.models import Cart
from apps.users.models import CustomUser


def get_shopping_cart_for(current_user: typing.Union[CustomUser, AnonymousUser]) -> Cart:
    """Return shopping for current user.

    Args:
        current_user: project auth user.
    """
    cart, _ = Cart.objects.prefetch_related('recipes').get_or_create(owner=current_user)
    return cart
