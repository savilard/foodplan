from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from apps.recipes.api.viewsets import IngredientViewSet
from apps.recipes.api.viewsets import RecipeViewSet
from apps.tags.api.viewsets import TagViewSet
from apps.users.api.viewsets import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('v1/', include(router.urls)),
]
