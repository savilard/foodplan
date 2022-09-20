from django.urls import include
from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.recipes.api.viewsets import IngredientViewSet
from apps.tags.api.viewsets import TagViewSet
from apps.users.api.viewsets import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('v1/', include(router.urls)),
]
