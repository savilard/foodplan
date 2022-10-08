from django_filters import rest_framework as filters

from apps.tags.models import Tag


class NumberInFilter(  # noqa: D101
    filters.BaseInFilter,
    filters.NumberFilter,
):
    pass  # noqa: WPS420, WPS604


class RecipeFilter(filters.FilterSet):
    """Recipe filter."""

    is_favorited = filters.BooleanFilter()
    is_in_shopping_cart = filters.BooleanFilter()
    author = NumberInFilter(field_name='author__id')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        fields = (
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
        )
