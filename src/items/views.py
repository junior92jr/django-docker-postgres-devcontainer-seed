from rest_framework import viewsets

from .models import Item
from .serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    """ViewSet for the Item model."""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
