from django.core.management.base import BaseCommand

from items.utils.price_sync import sync_all_items, sync_item_by_id


class Command(BaseCommand):
    help = (
        "Sync external_price for items. Use --item_id to sync a single item by ID. "
        "Without --item_id, syncs all items."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--item_id",
            type=int,
            help="ID of a single item to sync external price",
        )

    def handle(self, *args, **options):
        item_id = options.get("item_id")

        if item_id is not None:
            self.stdout.write(f"Syncing external price for item ID {item_id}...")
            result = sync_item_by_id(item_id, simulate_delay=False)
            self.stdout.write(result)
        else:
            self.stdout.write("Syncing external price for all items...")
            count = sync_all_items()
            self.stdout.write(
                self.style.SUCCESS(f"Updated external_price for {count} items.")
            )
