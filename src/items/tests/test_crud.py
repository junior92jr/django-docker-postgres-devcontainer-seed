from typing import Callable
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from items.models import Item


@pytest.fixture
def api_client() -> APIClient:
    """Fixture to provide an API client for testing."""
    return APIClient()


@pytest.fixture
def user(db) -> User:
    """Fixture to create a test user."""
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def authenticated_client(api_client: APIClient, user: User) -> APIClient:
    """Return an API client logged in as the test user."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def create_item() -> Callable[..., Item]:
    """Fixture to create an item in the database."""

    def _create_item(**kwargs) -> Item:
        return Item.objects.create(**kwargs)

    return _create_item


@pytest.mark.django_db
def test_list_items(
    authenticated_client: APIClient, create_item: Callable[..., Item]
) -> None:
    create_item(name="Item 1", description="desc", price=10.5)
    create_item(name="Item 2", description="desc2", price=20.0)

    url = reverse("item-list")
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 2


@pytest.mark.django_db
def test_create_item(authenticated_client: APIClient) -> None:
    url = reverse("item-list")
    data = {"name": "New Item", "description": "New description", "price": "15.99"}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == data["name"]
    assert float(response.data["price"]) == float(data["price"])


@pytest.mark.django_db
def test_retrieve_item(
    authenticated_client: APIClient, create_item: Callable[..., Item]
) -> None:
    """Test retrieving a single item."""
    item = create_item(name="Retrieve Item", description="desc", price=5.5)
    url = reverse("item-detail", args=[item.id])
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == item.id
    assert response.data["name"] == item.name


@pytest.mark.django_db
def test_update_item(
    authenticated_client: APIClient, create_item: Callable[..., Item]
) -> None:
    """Test updating an item."""
    item = create_item(name="Old Name", description="desc", price=7.0)
    url = reverse("item-detail", args=[item.id])
    data = {"name": "Updated Name", "description": "Updated desc", "price": "8.50"}
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == data["name"]
    assert float(response.data["price"]) == float(data["price"])


@pytest.mark.django_db
def test_delete_item(
    authenticated_client: APIClient, create_item: Callable[..., Item]
) -> None:
    """Test deleting an item."""
    item = create_item(name="Delete Me", description="desc", price=10.0)
    url = reverse("item-detail", args=[item.id])
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Item.objects.filter(id=item.id).exists()


@pytest.mark.django_db
@patch("items.views.simulate_external_price_sync_for_item.delay")
def test_sync_price(
    mock_task_delay, authenticated_client: APIClient, create_item: Callable[..., Item]
) -> None:
    """Test syncing price for a single item."""
    item = create_item(name="Test Item", description="desc", price=10.0)
    mock_task_delay.reset_mock()
    mock_task_delay.return_value.id = "fake-task-id"

    url = reverse("item-sync-price", args=[item.id])
    response = authenticated_client.post(url)

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.data["task_id"] == "fake-task-id"
    mock_task_delay.assert_called_once_with(item.id)


@pytest.mark.django_db
@patch("items.views.hourly_external_price_sync.delay")
def test_sync_all_prices(mock_task_delay, authenticated_client: APIClient) -> None:
    """Test syncing prices for all items."""
    mock_task_delay.reset_mock()
    mock_task_delay.return_value.id = "fake-batch-task-id"

    url = reverse("item-sync-all-prices")
    response = authenticated_client.post(url)

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.data["task_id"] == "fake-batch-task-id"
    mock_task_delay.assert_called_once()


@pytest.mark.django_db
@patch("items.views.AsyncResult")
def test_task_status(mock_async_result, authenticated_client: APIClient) -> None:
    """Test checking the status of a Celery task."""
    mock_result_instance = mock_async_result.return_value
    mock_result_instance.status = "SUCCESS"
    mock_result_instance.ready.return_value = True
    mock_result_instance.result = "done"

    task_id = "fake-task-id"
    url = reverse("item-task-status", args=[task_id])
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "task_id": task_id,
        "status": "SUCCESS",
        "result": "done",
    }
    mock_async_result.assert_called_once_with(task_id)
