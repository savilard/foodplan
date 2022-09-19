from django.contrib.auth.models import AbstractUser

from apps.core.models import BaseModel


class CustomUser(AbstractUser, BaseModel):
    """Custom user model."""

    pass

    def __str__(self):
        return self.username
