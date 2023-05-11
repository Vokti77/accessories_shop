from django.db import models
from django.utils import timezone

# Create your models here.
class Brand(models.Model):
    name = models.TextField(unique=True)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name
    
class Model(models.Model):
    name = models.TextField(unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,  blank=True, default=True)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_name = models.CharField(max_length=100, null=False, blank=False)
    model = models.ForeignKey(Model, on_delete=models.CASCADE,  blank=True, default=True)
    product_quantity = models.PositiveIntegerField(default=0)  # Initial product quantity
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_quantity = models.PositiveIntegerField(default=0)
    expecting_Saleing_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_Sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remining_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    added_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.product_quantity} X {self.product_name}"
    

class Sale(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, default=1)
    sale_quantity = models.PositiveIntegerField(default=0) 
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_Sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)


    

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Object is being updated
            original = Sale.objects.get(pk=self.pk)
            if original.sale_quantity != self.sale_quantity:
                # Sale_quantity has changed, update the update_at field
                self.update_at = timezone.now()
        super(Sale, self).save(*args, **kwargs)
