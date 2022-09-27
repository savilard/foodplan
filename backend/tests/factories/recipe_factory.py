import random

import factory


class RecipeIngredientFactory(factory.django.DjangoModelFactory):
    recipe = factory.SubFactory('tests.factories.RecipeFactory')
    ingredient = factory.SubFactory('tests.factories.IngredientFactory')
    amount = 1

    class Meta:
        model = 'recipes.RecipeIngredient'
        django_get_or_create = ['recipe', 'ingredient']


class RecipeTagFactory(factory.django.DjangoModelFactory):
    recipe = factory.SubFactory('tests.factories.RecipeFactory')
    tag = factory.SubFactory('tests.factories.TagFactory')

    class Meta:
        model = 'recipes.RecipeTag'
        django_get_or_create = ['recipe', 'tag']


class RecipeFactory(factory.django.DjangoModelFactory):
    author = factory.SubFactory('tests.factories.UserFactory')
    image = factory.django.ImageField()
    cooking_time = 2
    ingredients = factory.RelatedFactoryList(
        'tests.factories.RecipeIngredientFactory',
        factory_related_name='recipe',
        size=lambda: random.randint(1, 5),
    )
    tags = factory.RelatedFactoryList(
        'tests.factories.RecipeTagFactory',
        factory_related_name='recipe',
        size=lambda: random.randint(1, 5),
    )

    class Meta:
        model = 'recipes.Recipe'
