import re
from typing import Iterable

from django.db import models

from django_filters import rest_framework as filters

from apps.recipes.models import Ingredient


def normalize_query(query_string: str) -> Iterable[str]:
    """Splits the query string in individual keywords, getting rid of unnecessary spaces and grouping quoted words together.

     Args:
         query_string: query string

    Returns:
        object: query terms list
    """
    terms = re.compile(r'"([^"]+)"|(\S+)').findall
    normspace = re.compile(r'\s{2,}').sub
    return [
        normspace(' ', (term[0] or term[1]).strip())
        for term in terms(query_string)
    ]


def get_query(query_string: str, search_fields: Iterable[str]):
    """Returns a query, that is a combination of Q objects.

    That combination aims to search keywords within a model
    by testing the given search fields.
    """
    query = None
    for term in normalize_query(query_string):
        or_query = None
        for field_name in search_fields:
            search_query = models.Q(**{f'{field_name}__icontains': term})
            or_query = (
                search_query if or_query is None else search_query | or_query  # type: ignore
            )
        query = or_query if query is None else query & or_query  # type: ignore
    return query


class IngredientFilterSet(filters.FilterSet):
    """Filtering by partial occurrence at the beginning of an ingredient name."""

    name = filters.CharFilter(method='filter_query')

    def filter_query(self, queryset, name, search_value):
        """Custom filter query."""
        query = get_query(search_value, ['name'])
        return queryset.filter(query)

    class Meta:
        model = Ingredient
        fields = ('name',)
