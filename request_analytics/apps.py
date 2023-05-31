from django.apps import AppConfig


class RequestAnalyticsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "request_analytics"

    def ready(self):
        from . import erp
