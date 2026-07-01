from django import forms
from django_yearmonth_widget.widgets import DjangoYearMonthWidget

from accessories.models import Brand, Model, Product, Sale


class ProductsForm(forms.ModelForm):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all())
    model = forms.ModelChoiceField(queryset=Model.objects.none())

    class Meta:
        model = Product
        fields = [
            "product_name",
            "brand",
            "model",
            "product_quantity",
            "buying_price",
            "expecting_Saleing_price",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        brand_id = self.data.get("brand") or getattr(self.instance, "brand_id", None)
        if brand_id:
            self.fields["model"].queryset = Model.objects.filter(brand_id=brand_id)


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["sale_quantity", "sale_price"]


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name"]


class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ["name", "brand"]


class SearchForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["model"]


class ReportSearchForm(forms.ModelForm):
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)

    class Meta:
        model = Sale
        exclude = []
        widgets = {"published_yearmonth": DjangoYearMonthWidget()}
