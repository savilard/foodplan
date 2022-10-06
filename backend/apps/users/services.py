from apps.users.models import CustomUser


class UserService(object):
    """Service for project user."""

    def __init__(self, user: CustomUser, author: CustomUser) -> None:
        """Init for UserService.

        Args:
            user: authorized user;
            author: recipe author.
        """
        self.user = user
        self.author = author

    def add_follower(self):
        """Add a user to the recipe author's followers."""
        self.user.followers.add(self.author)

    def remove_follower(self):
        """Remove a user to the recipe author's followers."""
        self.user.followers.remove(self.author)
