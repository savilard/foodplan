from django.contrib.auth.models import AbstractUser

from apps.core.models import TimestampedModelWithUUID


class CustomUser(AbstractUser, TimestampedModelWithUUID):
    """Custom user model."""

    pass

    def __str__(self):
        return self.username
