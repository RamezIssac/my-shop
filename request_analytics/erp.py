from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Sum, Count
from django.utils.translation import gettext_lazy as _

from erp_framework.reporting.registry import register_report_view
from erp_framework.reporting.views import ReportView, ListReportView
from slick_reporting.fields import SlickReportField, TotalReportField

from request.models import Request
from slick_reporting.generator import Chart

from .forms import RequestLogForm


@register_report_view(admin_site_names=["requests-dashboard"])
class RequestLog(ListReportView):
    report_model = Request
    base_model = Request
    form_class = RequestLogForm
    report_title = "Request Log"
    date_field = "time"

    default_order_by = "-time"

    limit_records = 10

    columns = [
        "id",
        "method",
        "path",
        "user_agent",
        "user",
        "referer",
        ("get_time_verbose", {"verbose_name": "Time"}),
        "response",
    ]

    def get_time_verbose(self, obj):
        return naturaltime(obj.time)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


@register_report_view(admin_site_names=["requests-dashboard"])
class RequestCountByPath(ReportView):
    queryset = Request.objects.filter(response__lt=400)
    # report_model = Request
    report_title = "Request Count By Path"
    group_by = "path"
    date_field = "time"
    columns = [
        "path",
        SlickReportField.create(Count, "id", verbose_name="Total Count"),
    ]

    default_order_by = "-count__id"


@register_report_view(admin_site_names=["requests-dashboard"])
class RequestErrorCountByPath(ReportView):
    queryset = Request.objects.filter(response__in=[500])
    report_title = "Request Error Count By Path"
    group_by = "path"
    date_field = "time"
    columns = [
        "path",
        SlickReportField.create(Count, "id", verbose_name="Total Count"),
    ]

    default_order_by = "-count__id"


@register_report_view(admin_site_names=["requests-dashboard"])
class RequestCountByReferer(ReportView):
    report_model = Request
    report_title = "Request Count By Referer"
    group_by = "path"
    date_field = "time"
    columns = [
        "path",
        SlickReportField.create(Count, "id", verbose_name="Total Count"),
    ]


@register_report_view(admin_site_names=["requests-dashboard"])
class RequestCountByPathTimeSeries(RequestCountByPath):
    # report_model = Request
    report_title = "Request Count By Path [time series]"
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

    # default_order_by = ""


@register_report_view(admin_site_names=["requests-dashboard"])
class RequestsCountByUserAgent(ReportView):
    report_model = Request
    report_title = "Requests Count By User Agent"
    group_by = "user_agent"
    date_field = "time"
    columns = [
        "user_agent",
        SlickReportField.create(Count, "id", verbose_name="Total Count"),
    ]

    default_order_by = "-count__id"

    chart_settings = [
        Chart(
            "Browsers",
            Chart.PIE,
            title_source=["user_agent"],
            data_source=["count__id"],
            plot_total=True,
        ),
    ]

    # We can add time series mode to the report by
    # time_series_selector = True
    # time_series_selector_allow_empty = True
    # time_series_selector_default = ""
    #
    # time_series_columns = [
    #     SlickReportField.create(Count, "id", verbose_name="Total Count"),
    # ]
