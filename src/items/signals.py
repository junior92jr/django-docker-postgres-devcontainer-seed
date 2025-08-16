from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Item
from .tasks import simulate_external_price_sync_for_item


@receiver(post_save, sender=Item)
def trigger_external_price_sync(sender, instance, created, **kwargs):
    """Trigger external price sync task after Item is created."""
    # Only trigger the task if the Item is newly created
    # and not updated, to avoid unnecessary syncs.
    if created:
        simulate_external_price_sync_for_item.delay(instance.pk)
