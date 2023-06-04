from erp_framework.sites import DefaultERPSite
from erp_framework.admin.admin import ERPFrameworkAdminSite


class RequestsDashboard(ERPFrameworkAdminSite):
    index_template = "request_analytics/index.html"


requests_dashboard = RequestsDashboard(name="requests-dashboard")
