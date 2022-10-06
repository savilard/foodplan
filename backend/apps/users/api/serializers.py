from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from apps.users.models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    """Model serializer for creating custom user by djoser."""

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(serializers.ModelSerializer):
    """Model serializer for custom user."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, author: CustomUser) -> bool:  # noqa: WPS615
        """Checks if the user is subscribed to the author of the recipe.

        Args:
            author: recipe author.
        """
        user = self.context['request'].user
        if not user.is_anonymous:
            return user.followers.filter(id=author.id).exists()
