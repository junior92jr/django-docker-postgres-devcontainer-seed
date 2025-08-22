from celery.result import AsyncResult
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Item
from .serializers import ItemSerializer
from .tasks import (hourly_external_price_sync,
                    simulate_external_price_sync_for_item)


class ItemViewSet(viewsets.ModelViewSet):
    """ViewSet for managing items."""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filterset_fields = ["price"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def sync_price(self, request: Request, pk: str | None = None) -> Response:
        """
        Trigger external price sync for a single item (async).
        Returns the Celery task ID so it can be tracked.
        """
        task = simulate_external_price_sync_for_item.delay(int(pk))
        return Response(
            {"message": f"Price sync triggered for item {pk}", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED,
        )

    @action(detail=False, methods=["post"])
    def sync_all_prices(self, request: Request) -> Response:
        """
        Trigger external price sync for all items (async).
        """
        task = hourly_external_price_sync.delay()
        return Response(
            {"message": "Price sync triggered for all items", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED,
        )

    @action(detail=False, methods=["get"], url_path="task-status/(?P<task_id>[^/.]+)")
    def task_status(self, request: Request, task_id: str | None = None) -> Response:
        """
        Check the status of a Celery task by ID.
        Requires that CELERY_RESULT_BACKEND is configured.
        """
        result = AsyncResult(task_id)
        return Response(
            {
                "task_id": task_id,
                "status": result.status,
                "result": result.result if result.ready() else None,
            }
        )
