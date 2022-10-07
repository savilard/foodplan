from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Favorites(BaseModel):
    recipe = models.ForeignKey(
        'recipes.Recipe',
        related_name='favorites',
        verbose_name=_('Recipe'),
        on_delete=models.CASCADE,
        db_index=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='favorites',
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Favorites')
        verbose_name_plural = _('Favorites')
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'recipe',
                    'user',
                ),
                name='%(app_label)s_%(class)s_recipe_user_unique_together',
            ),
        )

    def __str__(self) -> str:
        return '{0}: {1}'.format(self.user.full_name, self.recipe.name)
