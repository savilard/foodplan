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
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed', read_only=True)

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

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return user.followers.filter(id=obj.id).exists()
