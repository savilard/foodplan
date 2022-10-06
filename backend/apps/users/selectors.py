from rest_framework.generics import get_object_or_404

from apps.users.models import CustomUser


def get_user_followers(user):
    """Get auth user followers.

    Args:
        user: auth user.
    """
    return user.followers.all()


def get_user_by(user_id: str) -> CustomUser:
    """Get user by id.

    Args:
        user_id: user id.
    """
    return get_object_or_404(CustomUser, id=user_id)


def is_user_subscribed_to_author(user: CustomUser, author: CustomUser) -> bool:
    """Checks if the user is subscribed to the specified author of the recipe.

    Args:
        user: auth project user;
        author: recipe author.
    """
    return user.followers.filter(id=author.id).exists()
