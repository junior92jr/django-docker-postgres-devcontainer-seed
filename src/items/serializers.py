from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for the Item model."""

    class Meta:
        """Meta options for the ItemSerializer."""

        model = Item
        fields = (
            "id",
            "name",
            "description",
            "price",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["created_at", "updated_at"]
