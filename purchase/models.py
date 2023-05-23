from django.db import models

from django.utils.translation import gettext_lazy as _


# Create your models here.


class Purchase(models.Model):
    number = models.CharField(max_length=100, verbose_name=_("Sale Number"))
    date = models.DateTimeField(verbose_name=_("Date"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))

    product = models.ForeignKey(
        "sales.Product", on_delete=models.CASCADE, verbose_name=_("Product")
    )
    quantity = models.IntegerField(verbose_name=_("Quantity"))
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Price"))
    value = models.DecimalField(
        max_digits=9, decimal_places=2, editable=False, verbose_name=_("Value")
    )

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        self.value = self.quantity * self.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Purchase")
        verbose_name_plural = _("Purchases")


class ProductInOutDBView(models.Model):
    date = models.DateTimeField(verbose_name=_("Date"))
    doc_type = models.CharField(max_length=20, verbose_name=_("Document Type"))
    product = models.ForeignKey(
        "sales.Product", on_delete=models.DO_NOTHING, verbose_name=_("Product")
    )
    quantity = models.IntegerField(verbose_name=_("Quantity"))
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Price"))
    value = models.DecimalField(
        max_digits=9, decimal_places=2, editable=False, verbose_name=_("Value")
    )

    class Meta:
        managed = False
        db_table = "product_in_out_view"
        verbose_name = "Product In Out View"
        verbose_name_plural = "Product In Out View"
        """
        create or replace view product_in_out_view as
        select id, date,  'sale' as doc_type, quantity , price, value from sales_sale
        union all
        select id , date, 'purchase' as doc_type , quantity , price, value from purchase_purchase
        """
