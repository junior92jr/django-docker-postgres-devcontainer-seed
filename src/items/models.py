from decimal import Decimal

from django.db import models


class Item(models.Model):
    """Model representing an item in the inventory."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    external_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Price from external system (simulated)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return a string representation of the item."""
        return f"{self.name}"

    class Meta:
        """Meta options for the Item model."""

        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="price_gte_0",
            ),
        ]
