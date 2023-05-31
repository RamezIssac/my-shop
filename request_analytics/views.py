from django.views.generic import TemplateView


class Dashboard(TemplateView):
    template_name = "front_end_dashboard.html"
