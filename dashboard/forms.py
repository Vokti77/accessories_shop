from django import forms

from accessories.models import Product, Sale, Brand

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'brand', 'model', 'product_quantity', 'buying_price', 'expecting_Saleing_price']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['sale_quantity', 'sale_price']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']   
