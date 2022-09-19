import uuid

from django.db import models

from behaviors.behaviors import Timestamped


class BaseModel(Timestamped):
    """
    Base app model that has `created` and `updated` attributes.

    Currently based on https://github.com/audiolion/django-behaviors
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
