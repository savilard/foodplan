from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class CustomUser(AbstractUser, BaseModel):  # type: ignore
    """Custom user model."""

    follow_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Who I follow'),
        related_name='followers',
        blank=True,
        symmetrical=False,
    )

    @property
    def full_name(self) -> str:
        """Return user first name and last name."""
        return f'{self.first_name} {self.last_name}'.strip()

    def __str__(self):
        return self.username
