from django.utils.translation import gettext_lazy as _

import pytest

from tests.factories import CartFactory, RecipeFactory

pytestmark = [pytest.mark.django_db]


def test_create_cart_successful(cart_factory: CartFactory, recipe_factory: RecipeFactory) -> None:
    """Test cart create."""
    recipes = recipe_factory.create_batch(size=5)
    cart = cart_factory.create(recipes=recipes)

    assert str(cart) == '{title}: {owner_full_name}'.format(
        title=_('Shopping list'),
        owner_full_name=cart.owner.full_name,
    )
    assert cart.recipes.count() == 5
