from django.db import models
from django.utils.translation import gettext_lazy as _


class Expense(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Expense Name"))

    class Meta:
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")

    def __str__(self):
        return self.name


class ExpenseTransaction(models.Model):
    number = models.CharField(max_length=100, verbose_name="Expense Transaction #")
    date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    expense = models.ForeignKey(
        Expense, on_delete=models.PROTECT, verbose_name=_("Expense")
    )
    value = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = _("Expense Transaction")
        verbose_name_plural = _("Expense Transactions")

    def __str__(self):
        return f"{self.number} - {self.date}"
