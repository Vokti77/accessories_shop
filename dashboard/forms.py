from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django_yearmonth_widget.widgets import DjangoYearMonthWidget
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
        fields = [ 'name','brand'] 

class SearchForm(forms.ModelForm): 
    
    class Meta:
        model = Product
        fields = ['model'] 


class ReportSearchForm(forms.ModelForm):
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    class Meta:
        model = Sale
        exclude = []
        widgets = {
            
            "published_yearmonth": DjangoYearMonthWidget(),
        }