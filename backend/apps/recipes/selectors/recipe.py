from apps.users.models import CustomUser


def get_recipes_for(current_user: CustomUser, queryset):
    """Returns recipes with the status of the user adding the recipe to favorites.

    Args:
        current_user: auth user;
        queryset: recipe queryset.
    """
    return (
        queryset.
        with_favorites_status(user=current_user).
        with_is_in_shopping_cart_status(user=current_user)
    )
