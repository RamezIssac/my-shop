import datetime
import random
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from sales.models import Client, Product, Sale


def date_range(start_date, end_date):
    for i in range((end_date - start_date).days + 1):
        yield start_date + timedelta(i)


class Command(BaseCommand):
    help = "Create Sample entries for the sales app"

    def handle(self, *args, **options):
        # create clients
        for i in range(1, 10):
            Client.objects.create(name=f"Client {i}")
        clients_ids = list(Client.objects.values_list("pk", flat=True))
        # create products
        for i in range(1, 10):
            Product.objects.create(name=f"Product {i}")
        products_ids = list(Product.objects.values_list("pk", flat=True))

        # create sales, 10 per day from start of the year

        start_date = datetime.datetime(2023, 1, 1)
        end_date = datetime.datetime.now() + timedelta(days=1)

        for date in date_range(start_date, end_date):
            for i in range(1, 10):
                Sale.objects.create(
                    client_id=random.choice(clients_ids),
                    product_id=random.choice(products_ids),
                    quantity=random.randint(1, 10),
                    price=random.randint(1, 100),
                    date=date,
                    number=f"Sale {date.strftime('%Y-%m-%d')} #{i}",
                )

        self.stdout.write(self.style.SUCCESS("Entries Created Successfully"))
