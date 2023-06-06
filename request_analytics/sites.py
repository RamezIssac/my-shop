from erp_framework.sites import DefaultERPSite
from erp_framework.admin.admin import ERPFrameworkAdminSite


class RequestsDashboard(ERPFrameworkAdminSite):
    pass  # sets the index template in the settings


requests_dashboard = RequestsDashboard(name="requests-dashboard")
