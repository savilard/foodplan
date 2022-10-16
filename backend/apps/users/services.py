from django.contrib.auth.models import AnonymousUser

from apps.users.models import CustomUser


class UserService(object):
    """Service for project user."""

    def __init__(self, user: CustomUser | AnonymousUser, author: CustomUser) -> None:
        """Init for UserService.

        Args:
            user: authorized user;
            author: recipe author.
        """
        self.user = user
        self.author = author

    def add_follower(self):
        """Add a user to the recipe author's followers."""
        if self.user.is_anonymous:
            return None
        return self.user.follow_by.add(self.author)

    def remove_follower(self):
        """Remove a user to the recipe author's followers."""
        if self.user.is_anonymous:
            return None
        return self.user.follow_by.remove(self.author)
