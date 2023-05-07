from django.contrib import admin
from erp_framework.admin.admin import erp_admin_site

from .models import Expense, ExpenseTransaction


# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    pass


erp_admin_site.register(Expense, ExpenseAdmin)


class ExpenseTransactionAdmin(admin.ModelAdmin):
    list_display = ['number', 'date', 'notes', 'expense', 'value']
    fields = ['number', 'date', 'expense', 'value', 'notes']
    list_filter = ['expense']
    date_hierarchy = 'date'
    search_fields = ['number', 'notes']

erp_admin_site.register(ExpenseTransaction, ExpenseTransactionAdmin)
