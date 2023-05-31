import datetime
from django import forms
from django.db.models import Q
from request.utils import HTTP_STATUS_CODES
from slick_reporting.form_factory import BaseReportForm


class RequestLogForm(BaseReportForm, forms.Form):
    SECURE_CHOICES = (
        ("all", "All"),
        ("secure", "Secure"),
        ("non-secure", "Not Secure"),
    )

    start_date = forms.DateField(
        required=False,
        label="Start Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_date = forms.DateField(
        required=False, label="End Date", widget=forms.DateInput(attrs={"type": "date"})
    )
    secure = forms.ChoiceField(
        choices=SECURE_CHOICES, required=False, label="Secure", initial="all"
    )
    method = forms.CharField(required=False, label="Method")
    response = forms.ChoiceField(
        choices=HTTP_STATUS_CODES,
        required=False,
        label="Response",
        initial="200",
    )
    other_people_only = forms.BooleanField(
        required=False, label="Show requests from other People Only"
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(RequestLogForm, self).__init__(*args, **kwargs)
        self.fields["start_date"].initial = datetime.date.today()
        self.fields["end_date"].initial = datetime.date.today()

    def get_filters(self):
        filters = {}
        q_filters = []
        if self.cleaned_data["secure"] == "secure":
            filters["is_secure"] = True
        elif self.cleaned_data["secure"] == "non-secure":
            filters["is_secure"] = False
        if self.cleaned_data["method"]:
            filters["method"] = self.cleaned_data["method"]
        if self.cleaned_data["response"]:
            filters["response"] = self.cleaned_data["response"]
        if self.cleaned_data["other_people_only"]:
            q_filters.append(~Q(user=self.request.user))

        return q_filters, filters

    def get_start_date(self):
        return self.cleaned_data["start_date"]

    def get_end_date(self):
        return self.cleaned_data["end_date"]
