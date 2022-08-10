REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user': 'apps.users.api.serializers.UserSerializer',
        'user_create': 'apps.users.api.serializers.CustomUserCreateSerializer',
        'current_user': 'apps.users.api.serializers.CurrentUserSerializer',
    },
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticated'],
    },
    'HIDE_USERS': False,
    'LOGOUT_ON_PASSWORD_CHANGE': True,
}
