from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimestampedModelWithUUID

models.CharField.register_lookup(models.functions.Length, 'len')


class Tag(TimestampedModelWithUUID):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200,
        unique=True,
        db_index=True,
        help_text=_('Tag name'),
    )
    color = models.CharField(
        verbose_name=_('Color'),
        max_length=7,
        unique=True,
        help_text=format_html(
            'Color HEX code (e.g. #49B64E) -> <a href="{url}" target="_blank">color-hex.com</a>',
            url='https://www.color-hex.com/',
        ),
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'color'),
                name='%(app_label)s_%(class)s_name_color_unique_together',
            ),
            models.CheckConstraint(
                check=models.Q(name__len__gt=0),
                name='%(app_label)s_%(class)s_name_is_empty',
            ),
            models.CheckConstraint(
                check=models.Q(color__startswith='#') & models.Q(color__len__in=(4, 7)),
                name='%(app_label)s_%(class)s_color_is_not_hex_code',
            ),
            models.CheckConstraint(
                check=models.Q(slug__len__gt=0),
                name='%(app_label)s_%(class)s_slug_is_empty',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name}'.strip()
