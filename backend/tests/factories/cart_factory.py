from collections.abc import Sequence
import typing

import factory

from apps.carts.models import Cart


class CartFactory(factory.django.DjangoModelFactory):
    """Cart factory."""

    owner = factory.SubFactory('tests.factories.UserFactory')

    class Meta:
        model = Cart

    @factory.post_generation
    def recipes(
        self,
        create: bool,
        extracted: Sequence[typing.Any],
        **kwargs: typing.Dict,
    ) -> None:
        if not create:
            return

        if extracted:
            for recipe in extracted:
                self.recipes.add(recipe)
