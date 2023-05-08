from django.db.models import Sum, Q
from django.utils.translation import gettext_lazy as _

from erp_framework.reporting.registry import register_report_view
from erp_framework.reporting.views import ReportView
from slick_reporting.fields import SlickReportField

from .models import Profitability


@register_report_view
class ProfitabilityReport(ReportView):
    report_title = _("Total Profitability Report")
    report_model = Profitability  # None #ExpenseReportModel
    base_model = Profitability

    group_by = "type"

    columns = ["type", SlickReportField.create(Sum, "value", verbose_name=_("Value"))]

    def get_doc_types_q_filters(self):
        return [Q(type__in=["saletransaction"])], [
            Q(type__in=["expensetransaction", "salereturn", "sales"])
        ]


@register_report_view
class ProfitabilityReportMonthly(ReportView):
    report_title = _("Profitability Report Monthly")
    report_model = Profitability  # None #ExpenseReportModel
    base_model = Profitability

    group_by = "type"
    # time_series_pattern = 'monthly'

    time_series_columns = [
        SlickReportField.create(Sum, "value", verbose_name=_("Value"), name="value")
    ]
    columns = [
        "type",
        "__time_series__",
        SlickReportField.create(Sum, "value", verbose_name=_("Value"), name="value"),
    ]

    time_series_selector = True
    time_series_selector_default = "monthly"

    chart_settings = [
        {
            "type": "column",
            "data_source": ["value"],  # todo change / address , unnatural data source
            "title_source": "type",
        },
        {
            "type": "column",
            "data_source": ["value"],  # todo change / address , unnatural data source
            "title_source": "type",
            "plot_total": True,
        },
    ]

    def get_doc_types_q_filters(self):
        return [Q(type__in=["saletransaction"])], [
            Q(type__in=["expensetransaction"])
        ]
