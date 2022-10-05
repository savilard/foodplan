import typing

from django.http import HttpRequest

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.api.serializers import CustomUserSerializer
from apps.users.models import CustomUser


class UserViewSet(DjoserUserViewSet):
    """ViewSet пользователя."""

    serializer_class = CustomUserSerializer

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
