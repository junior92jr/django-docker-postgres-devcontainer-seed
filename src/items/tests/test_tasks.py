from decimal import Decimal
from typing import List
from unittest.mock import MagicMock

import pytest

from items.models import Item
from items.tasks import (
    hourly_external_price_sync,
    simulate_external_price_sync_for_item,
)
from items.utils.price_sync import sync_all_items


@pytest.mark.django_db
def test_simulate_external_price_sync_for_item(mocker: MagicMock) -> None:
    """Test the simulation of external price synchronization for a specific item."""
    item: Item = Item.objects.create(name="Test Item", price=Decimal("100.00"))
    mock_sync: MagicMock = mocker.patch(
        "items.tasks.sync_item_by_id", return_value="mocked result"
    )

    result: str = simulate_external_price_sync_for_item(item.id)

    assert result == "mocked result"
    mock_sync.assert_called_once_with(item.id)


@pytest.mark.django_db
def test_hourly_external_price_sync(mocker: MagicMock) -> None:
    """Test the hourly external price synchronization task."""
    mock_sync_all: MagicMock = mocker.patch(
        "items.tasks.sync_all_items", return_value=3
    )

    result: str = hourly_external_price_sync()

    assert result == "Updated external_price for 3 items."
    mock_sync_all.assert_called_once_with()


@pytest.mark.django_db
def test_sync_item_by_id_updates_price() -> None:
    """Test that the external_price is updated for a specific item."""
    item: Item = Item.objects.create(
        name="Item1",
        price=Decimal("50.00"),
        external_price=Decimal("50.00"),
    )

    result: str = simulate_external_price_sync_for_item(item.id)
    item.refresh_from_db()

    assert "updated to" in result
    assert item.external_price != Decimal("50.00")


@pytest.mark.django_db
def test_sync_all_items_updates_all() -> None:
    """Test that all items are updated."""
    items: List[Item] = [
        Item.objects.create(
            name=f"Item{i}",
            price=Decimal("100.00"),
            external_price=Decimal("100.00"),
        )
        for i in range(5)
    ]

    count: int = sync_all_items(batch_size=2)

    assert count == len(items)
    for item in Item.objects.all():
        assert item.external_price is not None
