import typing

from django.http import HttpRequest

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.recipes.api.pagination import LimitPageNumberPagination
from apps.recipes.api.serializers import RecipeAuthorSerializer
from apps.users.api.serializers import CustomUserSerializer
from apps.users.models import CustomUser


class UserViewSet(DjoserUserViewSet):
    """ViewSet пользователя."""

    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPagination

    @action(methods=['post'], detail=True, permission_classes=(IsAuthenticated, ))
    def subscribe(self, request: HttpRequest, id: typing.Optional[str] = None):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)

        if user == author:
            return Response({'errors': 'You cannot subscribe to yourself'}, status=status.HTTP_400_BAD_REQUEST)

        if user.followers.filter(id=author.id).exists():
            return Response({'errors': 'You are already subscribed to this user'}, status=status.HTTP_400_BAD_REQUEST)

        user.followers.add(author)

        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request: HttpRequest, id: typing.Optional[str] = None):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)

        if user == author:
            return Response({'errors': 'Вы не можете отписаться от самого себя'}, status=status.HTTP_400_BAD_REQUEST)

        if user.followers.filter(id=author.id).exists():
            user.followers.remove(author)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'errors': 'Вы уже отписались'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, permission_classes=(IsAuthenticated, ))
    def subscriptions(self, request: HttpRequest):
        queryset = request.user.followers.all()
        pages = self.paginate_queryset(queryset)
        serializer = RecipeAuthorSerializer(pages, many=True, context={'request': request})

        return self.get_paginated_response(serializer.data)
