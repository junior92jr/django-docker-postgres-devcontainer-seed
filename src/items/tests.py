import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Item


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_item():
    def _create_item(**kwargs):
        return Item.objects.create(**kwargs)

    return _create_item


@pytest.mark.django_db
def test_list_items(api_client, create_item):
    create_item(name="Item 1", description="desc", price=10.5)
    create_item(name="Item 2", description="desc2", price=20.0)

    url = reverse("item-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 2


@pytest.mark.django_db
def test_create_item(api_client):
    url = reverse("item-list")
    data = {"name": "New Item", "description": "New description", "price": "15.99"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == data["name"]
    assert float(response.data["price"]) == float(data["price"])


@pytest.mark.django_db
def test_retrieve_item(api_client, create_item):
    item = create_item(name="Retrieve Item", description="desc", price=5.5)
    url = reverse("item-detail", args=[item.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == item.id
    assert response.data["name"] == item.name


@pytest.mark.django_db
def test_update_item(api_client, create_item):
    item = create_item(name="Old Name", description="desc", price=7.0)
    url = reverse("item-detail", args=[item.id])
    data = {"name": "Updated Name", "description": "Updated desc", "price": "8.50"}
    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == data["name"]
    assert float(response.data["price"]) == float(data["price"])


@pytest.mark.django_db
def test_delete_item(api_client, create_item):
    item = create_item(name="Delete Me", description="desc", price=10.0)
    url = reverse("item-detail", args=[item.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Confirm deletion
    assert not Item.objects.filter(id=item.id).exists()
