from django import forms

from accessories.models import Product,Sell

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'brand_name', 'product_quantity','buying_price', 'expecting_selling_price']

class SellForm(forms.ModelForm):
    class Meta:
        model = Sell
        fields = ['sell_quantity', 'sell_price']
