import random

from django.core.management.base import BaseCommand
from faker import Faker

from items.models import Item

fake = Faker()


class Command(BaseCommand):
    help = "Generate 100,000 fake items for testing"

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating 100,000 fake items...")

        items = []

        for _ in range(100000):
            created_at = fake.date_time_between(start_date="-2y", end_date="now")
            item = Item(
                name=fake.word().capitalize(),
                description=fake.sentence(),
                price=round(random.uniform(1.0, 1000.0), 2),
                created_at=created_at,
                updated_at=created_at,
            )
            items.append(item)

        Item.objects.bulk_create(items, batch_size=1000)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created 100,000 items with random timestamps"
            )
        )
