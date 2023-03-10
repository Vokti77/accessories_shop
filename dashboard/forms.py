from django import forms

from accessories.models import Product

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'brand_name', 'product_quantity','buying_price', 'expecting_selling_price']
