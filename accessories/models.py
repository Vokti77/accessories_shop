from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    brand_name = models.CharField(max_length=100)
    product_quantity = models.PositiveIntegerField(default=0)  # Initial product quantity
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expecting_selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remining_quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    sold_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.product_quantity} X {self.product_name}"

    


class Sell(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, default=1) 
    actual_selling_price = models.DecimalField(max_digits=10, decimal_places=2)

