from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["brand__name", "name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=100, db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="products")
    product_quantity = models.PositiveIntegerField()
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_quantity = models.PositiveIntegerField(default=0)
    expecting_Saleing_price = models.DecimalField(max_digits=10, decimal_places=2)
    actual_Sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remining_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    added_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-added_at", "product_name"]

    @property
    def current_profit(self):
        return self.actual_Sale_price - (self.sale_quantity * self.buying_price)

    def __str__(self):
        return f"{self.product_quantity} X {self.product_name}"


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")
    sale_quantity = models.PositiveIntegerField(default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_Sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_at = models.DateField()
    update_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-sale_at", "-id"]

    def clean(self):
        if self.product_id and self.sale_quantity > self.product.product_quantity:
            raise ValidationError("Sale quantity cannot exceed current stock quantity.")

    def calculate_totals(self):
        self.total_Sale_price = Decimal(self.sale_quantity) * self.sale_price
        self.profit = self.total_Sale_price - (
            Decimal(self.sale_quantity) * self.product.buying_price
        )

    def save(self, *args, **kwargs):
        self.calculate_totals()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.sale_quantity}"


class ProductQuantityHistory(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="quantity_history"
    )
    quantity_added = models.PositiveIntegerField()
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-added_at", "-id"]

    def __str__(self):
        return f"{self.quantity_added} added to {self.product.product_name} at {self.added_at}"


class MonthlySaleProfitHistory(models.Model):
    stock_quantity = models.PositiveIntegerField()
    stock_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_quantity = models.PositiveBigIntegerField()
    sale_amount = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-date_added"]
