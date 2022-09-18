from django.template.defaultfilters import slugify

from factory import Faker
from factory import LazyAttribute
from factory.django import DjangoModelFactory

from apps.tags.models import Tag
from tests.factories.mixins import UniqueStringMixin


class TagFactory(DjangoModelFactory):
    """Tag factory."""

    name = UniqueStringMixin('word')
    color = Faker('color', hue='orange', luminosity='bright')
    slug = LazyAttribute(lambda tag: slugify(tag.name))

    class Meta:
        model = Tag
