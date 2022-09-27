from typing import Any, Sequence

from django.conf import settings

import factory

PASSWORD_LENGTH = 42


class UserFactory(factory.django.DjangoModelFactory):
    """Custom user factory."""

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_staff = False

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)

    @factory.post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else factory.Faker(
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
