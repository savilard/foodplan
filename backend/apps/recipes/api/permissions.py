from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.recipes.models import Recipe


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, recipe: Recipe):
        return request.method in SAFE_METHODS or recipe.author == request.user
