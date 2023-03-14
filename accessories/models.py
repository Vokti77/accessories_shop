from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    brand_name = models.CharField(max_length=100)
    product_quantity = models.PositiveIntegerField(default=0)  # Initial product quantity
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_quantity = models.PositiveIntegerField(default=0)
    expecting_selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_sell_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remining_quantity = models.PositiveIntegerField(default=0)
    added_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.product_quantity} X {self.product_name}"

class Sell(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, default=1)
    sell_quantity = models.PositiveIntegerField(default=0) 
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_sell_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sell_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Object is being updated
            original = Sell.objects.get(pk=self.pk)
            if original.sell_quantity != self.sell_quantity:
                # sell_quantity has changed, update the update_at field
                self.update_at = timezone.now()
        super(Sell, self).save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     self.total_sell_price += self.sell_quantity * self.actual_sell_price
    #     super(Sell, self).save(*args, **kwargs)