from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Cart(BaseModel):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='cart',
        verbose_name=_('Owner'),
        on_delete=models.CASCADE,
    )
    recipes = models.ManyToManyField(
        'recipes.Recipe',
        verbose_name=_('Recipes'),
        related_name='carts',
    )

    class Meta:
        verbose_name = _('Shopping list')
        verbose_name_plural = _('Shopping lists')

    def __str__(self) -> str:
        return '_("Shopping list"): {owner_full_name}'.format(owner_full_name=self.owner.full_name)
