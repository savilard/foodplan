from rest_framework import viewsets

from apps.tags.api.serializers import TagSerializer
from apps.tags.models import Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Get a list of tags and a tag by its id.

    Only admins are allowed to create and edit tags
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
