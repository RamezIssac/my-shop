from django.db import models
from django.utils.translation import gettext_lazy as _
from erp_framework.base.models import EntityModel


# Create your models here.
class Client(EntityModel):
    # name = models.CharField(max_length=100, verbose_name='Client Name')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Product Name")

    def __str__(self):
        return self.name


class Sale(models.Model):
    number = models.CharField(max_length=100, verbose_name="Sale Number")
    date = models.DateTimeField(verbose_name=_("Date"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name=_("Client")
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_("Product")
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
