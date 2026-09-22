"""
One-shot demo seeding: a demo login plus all sample data.

Wraps the app-provided seed commands so onboarding is a single step:

    python manage.py migrate
    python manage.py seed_demo
    python manage.py runserver

Creates (idempotently) the demo superuser ``test`` / ``testuser123``
advertised on the login page, then delegates to ``create_entries`` and
``create_purchase_entries`` for the sales / purchase / expense sample data.
"""
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

DEMO_USERNAME = "test"
DEMO_PASSWORD = "testuser123"


class Command(BaseCommand):
    help = "Seed the demo: demo login (test/testuser123) plus all sample data"

    def handle(self, *args, **options):
        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=DEMO_USERNAME,
            defaults={"is_staff": True, "is_superuser": True},
        )
        # create_entries deletes non-superusers, so make sure the demo login
        # is (and stays) a superuser with the documented password.
        changed = False
        if not (user.is_staff and user.is_superuser):
            user.is_staff = True
            user.is_superuser = True
            changed = True
        user.set_password(DEMO_PASSWORD)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Demo login ready: username '{DEMO_USERNAME}' "
                f"password '{DEMO_PASSWORD}'"
            )
        )

        call_command("create_entries")
        call_command("create_purchase_entries")

        self.stdout.write(
            self.style.SUCCESS(
                "Demo seeded. Run 'python manage.py runserver' and log in "
                f"at / with '{DEMO_USERNAME}' / '{DEMO_PASSWORD}'."
            )
        )
