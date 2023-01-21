from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100,unique=True,null=False,blank=False)
    brand_name = models.CharField(max_length=100)
    product_quantity = models.PositiveIntegerField(default=0)  # Initial product quantity
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expecting_selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remining_quantity = models.PositiveIntegerField(default=0)
    quantity_update_date = models.DateField(auto_now_add=True)
    remining_quantity_date = models.DateField(auto_now=True)

    # profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # sell_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product_quantity} X {self.product_name}"


class Sell(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, default=1) 
    actual_selling_price = models.DecimalField(max_digits=10, decimal_places=2)

