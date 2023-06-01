from django.db.models import Sum, Count
from django.utils.translation import gettext_lazy as _
from slick_reporting.views import SlickReportingListView

from erp_framework.reporting.registry import register_report_view
from erp_framework.reporting.views import ReportView
from slick_reporting.fields import SlickReportField, TotalReportField

from request.models import Request
from .forms import RequestLogForm


@register_report_view
class RequestLog(SlickReportingListView):
    report_model = Request
    base_model = Request
    form_class = RequestLogForm
    report_title = "Request Log"
    date_field = "time"

    columns = [
        "id",
        "method",
        "path",
        "user_agent",
        "user",
        "referer",
        "time",
    ]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


@register_report_view
class RequestCountByPath(ReportView):
    report_model = Request
    report_title = "Request Count By Path"
    group_by = "path"
    date_field = "time"
    columns = [
        "path",
        SlickReportField.create(Sum, "id", verbose_name="Total Count"),
    ]


@register_report_view
class RequestCountByPathTimeSeries(RequestCountByPath):
    report_model = Request
    report_title = "Request Count By Path"
    group_by = "path"
    date_field = "time"
    time_series_selector = True
    time_series_columns = [
        SlickReportField.create(Count, "id", verbose_name="Total Count"),
    ]

    columns = [
        "path",
        SlickReportField.create(Count, "id", verbose_name="Total Count"),
    ]
