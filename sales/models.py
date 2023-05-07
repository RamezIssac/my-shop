from django.db import models


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Client Name')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Product Name')

    def __str__(self):
        return self.name


class Sale(models.Model):
    number = models.CharField(max_length=100, verbose_name='Sale Number')
    date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    value = models.DecimalField(max_digits=9, decimal_places=2, editable=False)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        self.value = self.quantity * self.price
        super(Sale, self).save(*args, **kwargs)


