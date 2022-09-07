from djoser.serializers import UserCreateSerializer

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
