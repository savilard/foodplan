from django.http import HttpRequest
from django.http import HttpResponse

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.recipes.api.pagination import LimitPageNumberPagination
from apps.recipes.api.serializers import RecipeAuthorSerializer
from apps.users.api.serializers import CustomUserSerializer
from apps.users.selectors import get_user_by
from apps.users.selectors import get_user_followers
from apps.users.selectors import is_user_subscribed_to_author
from apps.users.services import UserService


class UserViewSet(DjoserUserViewSet):
    """Custom user ViewSet."""

    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPagination

    @action(methods=['post'], detail=True, permission_classes=(IsAuthenticated,))
    def subscribe(self, request: HttpRequest, id: str | None = None) -> HttpResponse:  # noqa: WPS125
        """Allows an authorized user to subscribe to the author of a recipe.

        Args:
            request (object): Django http request,
            id (str): The id of the author of the recipe to which the user subscribes
        """
        user = request.user
        author = get_user_by(user_id=id)
        service = UserService(user=user, author=author)

        if user == author:
            return Response(
                {'errors': 'You cannot subscribe to yourself'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if is_user_subscribed_to_author(user=user, author=author):
            return Response(
                {'errors': 'You are already subscribed to this user'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service.add_follower()

        serializer = RecipeAuthorSerializer(author, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request: HttpRequest, id: str | None = None) -> HttpResponse:  # noqa: WPS125
        """Allows an authorized user to unsubscribe to the author of a recipe.

        Args:
            request (object): Django http request,
            id (str): The id of the author of the recipe from which the user is unsubscribing
        """
        user = request.user
        author = get_user_by(user_id=id)
        service = UserService(user=user, author=author)

        if user == author:
            return Response(
                {'errors': 'Вы не можете отписаться от самого себя'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if is_user_subscribed_to_author(user=user, author=author):
            service.remove_follower()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'errors': 'Вы Уже отписались от автора'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(methods=['get'], detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request: HttpRequest) -> HttpResponse:
        """Get users that the current user is subscribed to.

        Args:
            request (object): Django http request,
        """
        queryset = get_user_followers(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = RecipeAuthorSerializer(
            pages,
            many=True,
            context={'request': request},
        )

        return self.get_paginated_response(serializer.data)
