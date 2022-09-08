from typing import Any, Sequence

from django.conf import settings

from factory import Faker
from factory import post_generation
from factory.django import DjangoModelFactory

PASSWORD_LENGTH = 42


class UserFactory(DjangoModelFactory):
    """Custom user factory."""

    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    is_staff = False

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                'password',
                length=PASSWORD_LENGTH,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={'locale': None})
        )
        self.set_password(password)

    @classmethod
    def build_payload(cls, user=None, user_email=None, user_password=None):
        user = user if user else cls.build()
        user_email = user_email if user_email else user.email
        user_password = user_password if user_password else user.password

        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user_email,
            'password': user_password,
        }
