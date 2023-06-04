from django.db.models import Sum, Q, Avg
from django.utils.translation import gettext_lazy as _

from erp_framework.doc_types import doc_type_registry, DocType
from erp_framework.reporting.registry import register_report_view
from erp_framework.reporting.views import ReportView
from slick_reporting.fields import SlickReportField
from slick_reporting.views import Chart

from sales.models import Product
from .models import Purchase, ProductInOutDBView


@register_report_view()
class ProductAveragePrice(ReportView):
    report_title = _("Product Average Price")
    report_model = Purchase

    group_by = "product"

    columns = [
        "name",
        SlickReportField.create(Avg, "price", verbose_name=_("Average Price")),
    ]


@register_report_view
class ProductAveragePriceMonthly(ProductAveragePrice):
    report_title = _("Product Average Price [Time Series selector]")
    time_series_selector = True
    time_series_selector_default = "monthly"

    time_series_columns = [
        SlickReportField.create(
            Avg, "price", verbose_name=_("Average Price"), name="price"
        )
    ]

    chart_settings = [
        Chart(_("Average Price"), Chart.COLUMN, ["price"], ["name"]),
        Chart(
            _("Average Price Total"), Chart.COLUMN, ["price"], ["name"], plot_total=True
        ),
    ]


@doc_type_registry.register
class SalesTransaction(DocType):
    name = "purchase"
    verbose_name = _("Purchase")
    plus_side = (Product,)


@register_report_view
class ProductMovementStatement(ReportView):
    report_title = _("Product Movement Statement")
    report_model = ProductInOutDBView
    base_model = Product

    group_by = "product"

    doc_type_plus_list = ["purchase"]
    doc_type_minus_list = ["sale"]
    # doc_type_field_name = "doc_type"

    columns = [
        "name",
        "__fb_quantity__",
        "__debit_quantity__",
        "__credit_quantity__",
        "__total_quantity__",
        "__balance_quantity__",
    ]

    chart_settings = [
        Chart(
            _("Quantity Pie Chart"),
            Chart.PIE,
            ["__total_quantity__"],
            ["name"],
        ),
    ]
