import random
import time
from decimal import ROUND_HALF_UP, Decimal
from typing import Iterator, List

from django.db import transaction

from items.models import Item


def simulate_external_price(base_price: Decimal) -> Decimal:
    """
    Generate a simulated external price with ±10% variation.
    """
    variation = random.uniform(-0.10, 0.10)
    new_price = base_price * Decimal(1 + variation)
    return new_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def chunked(iterable: List[Item], size: int) -> Iterator[List[Item]]:
    """
    Yield successive chunks from a list of Items.
    """
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]


def sync_item_by_id(item_id: int, simulate_delay: bool = True) -> str:
    """
    Sync external_price for a single Item by ID.
    Optionally simulate network/API delay.
    """
    try:
        with transaction.atomic():
            item = Item.objects.select_for_update().get(pk=item_id)

            if simulate_delay:
                time.sleep(random.uniform(0.1, 0.5))

            item.external_price = simulate_external_price(item.price)
            item.save()

            return f"External price for '{item.name}' updated to {item.external_price}"

    except Item.DoesNotExist:
        return f"Item with ID {item_id} does not exist."


def sync_all_items(batch_size: int = 500) -> int:
    """
    Update external_price for all Items in the database in batches.
    Returns the number of updated items.
    """
    updated_items: List[Item] = []

    for item in Item.objects.all().iterator():
        item.external_price = simulate_external_price(item.price)
        updated_items.append(item)

    for batch in chunked(updated_items, batch_size):
        with transaction.atomic():
            Item.objects.bulk_update(batch, ["external_price"])

    return len(updated_items)
