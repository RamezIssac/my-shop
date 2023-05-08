from django.db import models

# Create your models here.


class Purchase(models.Model):
    number = models.CharField(max_length=100, verbose_name='Sale Number')
    date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    product = models.ForeignKey("sales.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    value = models.DecimalField(max_digits=9, decimal_places=2, editable=False)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        self.value = self.quantity * self.price
        super().save(*args, **kwargs)

