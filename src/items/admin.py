from django.contrib import admin, messages

from .models import Item
from .tasks import hourly_external_price_sync


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "external_price", "updated_at")
    actions = ["run_external_price_sync"]

    @admin.action(description="Run external price sync task (now)")
    def run_external_price_sync(self, request, queryset):
        hourly_external_price_sync.delay()
        self.message_user(
            request,
            "External price sync task has been triggered.",
            messages.SUCCESS,
        )
