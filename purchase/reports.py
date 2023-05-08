from django.db.models import Sum, Q, Avg
from django.utils.translation import gettext_lazy as _

from erp_framework.reporting.registry import register_report_view
from erp_framework.reporting.views import ReportView
from slick_reporting.fields import SlickReportField
from slick_reporting.views import Chart

from sales.models import Product
from .models import Purchase


@register_report_view
class ProductAveragePrice(ReportView):
    report_title = _("Product Average Price")
    report_model = Purchase
    base_model = Product

    group_by = "product"

    columns = ["name", SlickReportField.create(Avg, "price", verbose_name=_("Average Price"))]


@register_report_view
class ProductAveragePriceMonthly(ProductAveragePrice):
    time_series_selector = True
    time_series_selector_default = "monthly"

    time_series_columns = [
        SlickReportField.create(Avg, "price", verbose_name=_("Average Price"), name="price")
    ]

    chart_settings = [
        Chart(_("Average Price"), Chart.COLUMN, ["price"], ["name"]),
        Chart(_("Average Price Total"), Chart.COLUMN, ["price"], ["name"], plot_total=True),
    ]


@register_report_view
class ProductMovementStatement(ReportView):
    report_title = _("Product Movement Statement")
    report_model = Purchase
    base_model = Product

    group_by = "product"

    columns = [
        "name",
        '__debit__', '__credit__',

    ]

