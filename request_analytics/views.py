from django.views.generic import TemplateView


class Dashboard(TemplateView):
    template_name = "request_analytics/index.html"
