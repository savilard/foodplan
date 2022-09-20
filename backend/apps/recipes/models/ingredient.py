from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Ingredient(BaseModel):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200,
        db_index=True,
    )
    measurement_unit = models.CharField(
        verbose_name=_('Measurement unit'),
        max_length=200,
        help_text=_('For example, a kilogram'),
    )

    class Meta:
        verbose_name = _('Measurement unit')
        verbose_name_plural = _('Measurement units')
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='%(app_label)s_%(class)s_name_measurement_unit_unique_together',
            ),
            models.CheckConstraint(
                check=models.Q(name__len__gt=0),
                name='%(app_label)s_%(class)s_name_is_empty',
            ),
            models.CheckConstraint(
                check=models.Q(measurement_unit__len__gt=0),
                name='%(app_label)s_%(class)s_measurement_unit_is_empty',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'.strip()
