from django.contrib import admin
from erp_framework.admin.admin import EntityAdmin

from .models import Client, Product, Sale
from erp_framework.sites import erp_admin_site

# Register your models here.
erp_admin_site.register(Client, EntityAdmin)
erp_admin_site.register(Product)


class SaleAdmin(admin.ModelAdmin):
    list_display = ["number", "date", "client", "product", "quantity", "price", "value"]
    list_display_links = ["number"]
    list_filter = ["client", "product", "date"]
    search_fields = ["number", "client__name", "product__name"]
    date_hierarchy = "date"
    fields = ["number", "date", "client", "product", "quantity", "price", "value"]
    readonly_fields = ["value"]


erp_admin_site.register(Sale, SaleAdmin)
