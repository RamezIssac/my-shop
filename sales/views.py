from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from erp_framework.reporting.registry import register_report_view
from erp_framework.reporting.views import ReportView
from slick_reporting.fields import SlickReportField

# Create your views here.
from .models import Sale, Product


@register_report_view
class SaleListReportView(ReportView):
    report_model = Sale
    base_model = Sale
    report_title = 'Sales List'
    columns = ['number', 'date', 'client', 'product', 'quantity', 'price', 'value']


@register_report_view
class TotalProductSales(ReportView):
    # the model to use for the report
    report_model = Sale
    base_model = Product

    # the field to use for the date
    date_field = 'date'

    report_title = 'Total Product Sales'

    # the field to use for the group by
    group_by = 'product'

    # Columns to display ,
    columns = ['name', SlickReportField.create(Sum, 'value', verbose_name='Total Value')]


@register_report_view
class TotalProductSalesTimeSeries(ReportView):
    # the model to use for the report
    report_model = Sale
    base_model = Product

    # the field to use for the date
    date_field = 'date'

    report_title = 'Product SalesTime Series'

    # the field to use for the group by
    group_by = 'product'

    # Columns to display ,
    columns = ['name',
               '__time_series__',
               SlickReportField.create(Sum, 'value', verbose_name='Total Value')]

    time_series_selector = True
    time_series_selector_default = "monthly"

    time_series_columns = [
        SlickReportField.create(Sum, "value", verbose_name=_("Value"), name="value")
    ]

    chart_settings = [
        {
            "type": "column",
            "data_source": ["value"],
            "title_source": "type",
        },
        {
            "title": "Total",
            'engine_name': 'chartsjs',
            "type": "column",
            "data_source": ["value"],
            "title_source": "type",
            "plot_total": True,
        },
        {
            "title": "Total",
            'engine_name': 'chartsjs',
            "type": "pie",
            "data_source": ["value"],
            "title_source": "type",
            "plot_total": True,
        },

    ]
