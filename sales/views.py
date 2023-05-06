from django.db.models import Sum
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
