import factory


class FavoritesFactory(factory.django.DjangoModelFactory):
    """Favorites factory."""

    user = factory.SubFactory('tests.factories.UserFactory')
    recipe = factory.SubFactory('tests.factories.RecipeFactory')

    class Meta:
        model = 'favorites.Favorites'
