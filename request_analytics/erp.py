from django.db.models import Sum
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
    # filters = ["method"]

    columns = [
        "id",
        "method",
        "path",
        # "query_params",
        # "data",
        "user_agent",
        "user",
        "referer",
        "time",
    ]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
