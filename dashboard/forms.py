from django import forms

from accessories.models import Product, Sale, Brand, Model

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'model', 'product_quantity', 'buying_price', 'expecting_Saleing_price']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['sale_quantity', 'sale_price']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']   
    
class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['name', 'brand'] 

class SearchForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['model'] 
