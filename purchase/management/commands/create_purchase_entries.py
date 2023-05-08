import datetime
import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from expense.models import Expense, ExpenseTransaction
from purchase.models import Purchase
from sales.models import Client, Product, Sale

User = get_user_model()


def date_range(start_date, end_date):
    for i in range((end_date - start_date).days + 1):
        yield start_date + timedelta(i)


class Command(BaseCommand):
    help = "Create Sample entries for the sales app"

    def handle(self, *args, **options):
        # create clients
        products_ids = list(Product.objects.values_list("pk", flat=True))

        start_date = datetime.datetime(2023, 1, 1)
        end_date = datetime.datetime.now() + timedelta(days=1)

        for date in date_range(start_date, end_date):
            for i in range(1, 10):
                product_id = random.choice(products_ids)
                # price = calculate_price(product_id)

                Purchase.objects.create(
                    product_id=random.choice(products_ids),
                    quantity=random.randint(1, 10),
                    price=random.randint(1, 100),
                    date=date,
                    number=f"Purchase{date.strftime('%Y-%m-%d')} #{i}",
                )

        self.stdout.write(self.style.SUCCESS("Entries Created Successfully"))
