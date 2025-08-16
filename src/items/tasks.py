from celery import shared_task

from items.utils.price_sync import sync_all_items, sync_item_by_id


@shared_task
def simulate_external_price_sync_for_item(item_id: int) -> str:
    """Simulate external price sync for a single Item by ID."""

    return sync_item_by_id(item_id)


@shared_task
def hourly_external_price_sync() -> str:
    """Run hourly external price sync for all Items."""

    count = sync_all_items()
    return f"Updated external_price for {count} items."
