from django.template.defaultfilters import slugify

import factory

from tests.factories.mixins import UniqueStringMixin


class TagFactory(factory.django.DjangoModelFactory):
    """Tag factory."""

    name = UniqueStringMixin('word')
    color = factory.Faker('color', hue='orange', luminosity='bright')
    slug = factory.LazyAttribute(lambda tag: slugify(tag.name))

    class Meta:
        model = 'tags.Tag'
