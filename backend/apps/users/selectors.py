import typing

from django.contrib.auth.models import AnonymousUser
from django.db.models.query import QuerySet

from rest_framework.generics import get_object_or_404

from apps.users.models import CustomUser


def get_user_followers(
    user: typing.Union[CustomUser, AnonymousUser],
) -> typing.Optional['QuerySet[CustomUser]']:
    """Get auth user followers.

    Args:
        user: auth user.
    """
    if user.is_anonymous:
        return None
    return user.follow_by.all()


def get_user_by(user_id: typing.Optional[str]) -> CustomUser:
    """Get user by id.

    Args:
        user_id: user id.
    """
    return get_object_or_404(CustomUser, id=user_id)


def is_user_subscribed_to_author(
    user: typing.Union[CustomUser, AnonymousUser],
    author: CustomUser,
) -> typing.Optional[bool]:
    """Checks if the user is subscribed to the specified author of the recipe.

    Args:
        user: auth project user;
        author: recipe author.
    """
    if user.is_anonymous:
        return None
    return user.follow_by.filter(id=author.id).exists()