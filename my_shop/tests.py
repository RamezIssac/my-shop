"""
Smoke tests for the deployment contract and the demo's key pages.
"""
import datetime
import os
import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.conf import settings
from django.utils.timezone import now

from expense.models import Expense, ExpenseTransaction


class SettingsContractTests(TestCase):
    def test_static_and_media_urls(self):
        self.assertEqual(settings.STATIC_URL, "/static/")
        self.assertEqual(settings.MEDIA_URL, "/media/")

    def test_behind_proxy_https_settings(self):
        self.assertEqual(
            settings.SECURE_PROXY_SSL_HEADER, ("HTTP_X_FORWARDED_PROTO", "https")
        )
        self.assertTrue(settings.USE_X_FORWARDED_HOST)
        # Django's test runner appends "testserver" to ALLOWED_HOSTS after
        # settings are loaded; it is not part of the env-derived contract.
        env_hosts = [h for h in settings.ALLOWED_HOSTS if h != "testserver"]
        self.assertEqual(
            settings.CSRF_TRUSTED_ORIGINS,
            [f"https://{host}" for host in env_hosts if host and host != "*"],
        )

    @unittest.skipIf(
        os.environ.get("POSTGRES_DB"), "POSTGRES_DB set: checkout uses Postgres"
    )
    def test_sqlite_fallback_when_postgres_db_unset(self):
        self.assertEqual(
            settings.DATABASES["default"]["ENGINE"], "django.db.backends.sqlite3"
        )

    def test_debug_cast_to_bool(self):
        self.assertIsInstance(settings.DEBUG, bool)

    def test_wsgi_asgi_importable(self):
        import importlib

        self.assertIsNotNone(importlib.import_module("my_shop.wsgi").application)
        self.assertIsNotNone(importlib.import_module("my_shop.asgi").application)


class PageRenderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="pass"
        )

    def test_admin_login_page_renders(self):
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 200)

    def test_erp_index_redirects_anonymous_to_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_erp_index_renders_for_staff(self):
        self.client.login(username="admin", password="pass")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_report_page_renders(self):
        self.client.login(username="admin", password="pass")
        response = self.client.get("/reports/expense/expenses_daily/")
        self.assertEqual(response.status_code, 200)

    def test_daily_report_data_endpoints(self):
        """The showcased daily time-series reports must serve JSON data rows.

        Regression: under slick-reporting 1.4 these endpoints 500 with
        ImproperlyConfigured when the report class sets a time_series_pattern
        without a date_field.
        """
        expense = Expense.objects.create(name="Operations")
        ExpenseTransaction.objects.create(
            number="EX-1", date=now(), expense=expense, value="10.00"
        )
        self.client.login(username="admin", password="pass")
        params = {
            "start_date": (now() - datetime.timedelta(days=7)).date().isoformat(),
            "end_date": (now() + datetime.timedelta(days=1)).date().isoformat(),
        }
        for slug in ("expenses_daily", "expenses_daily_total"):
            with self.subTest(slug=slug):
                response = self.client.get(
                    f"/reports/expense/{slug}/",
                    params,
                    HTTP_X_REQUESTED_WITH="XMLHttpRequest",
                )
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.json()["data"])
