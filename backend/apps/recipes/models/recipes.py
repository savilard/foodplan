from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.recipes.managers import RecipeQuerySet


class Recipe(BaseModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='recipes',
        verbose_name=_('Author'),
        on_delete=models.CASCADE,
        db_index=True,
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200,
        db_index=True,
    )
    text = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(
        verbose_name=_('Image'),
        upload_to='recipes/images',
    )
    ingredients = models.ManyToManyField(
        'recipes.Ingredient',
        verbose_name=_('Ingredients'),
        related_name='recipes',
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField(
        'tags.Tag',
        verbose_name=_('Tags'),
        related_name='recipes',
        through='RecipeTag',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=_('Cooking time'),
        validators=[
            MinValueValidator(1),
        ],
        help_text=_('In minutes.'),
    )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        ordering = ('-created',)

    def __str__(self) -> str:
        return str(self.name).strip()


class RecipeIngredient(BaseModel):
    recipe = models.ForeignKey(
        'recipes.Recipe',
        verbose_name=_('Recipe'),
        related_name='recipe_ingredients',
        on_delete=models.CASCADE,
        db_index=True,
    )
    ingredient = models.ForeignKey(
        'recipes.Ingredient',
        verbose_name=_('Ingredient'),
        related_name='recipe_ingredients',
        on_delete=models.PROTECT,
        db_index=True,
    )
    amount = models.PositiveIntegerField(verbose_name=_('Amount'))

    class Meta:
        verbose_name = _('Recipe ingredient')
        verbose_name_plural = _('Recipe ingredients')
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'ingredient',
                    'recipe',
                ),
                name='%(app_label)s_%(class)s_recipe_ingredient_unique_together',
            ),
            models.CheckConstraint(
                check=models.Q(amount__gt=0),
                name='%(app_label)s_%(class)s_amount_less_than_one',
            ),
        )

    def __str__(self) -> str:
        return f'{self.recipe}: {self.ingredient.name}, {self.amount}'.strip()


class RecipeTag(BaseModel):
    recipe = models.ForeignKey(
        'recipes.Recipe',
        verbose_name=_('Recipe'),
        related_name='recipe_tags',
        on_delete=models.CASCADE,
        db_index=True,
    )
    tag = models.ForeignKey(
        'tags.Tag',
        verbose_name=_('Tag'),
        related_name='recipe_tags',
        on_delete=models.PROTECT,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Recipe tag')
        verbose_name_plural = _('Recipe tags')
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'recipe',
                    'tag',
                ),
                name='%(app_label)s_%(class)s_recipe_tag_unique_together',
            ),
        )

    def __str__(self) -> str:
        return f'{self.recipe}: {self.tag}'.strip()
