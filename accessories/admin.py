from django.contrib import admin
from accessories.models import Brand, Product, Sale, Model, ProductQuantityHistory, MonthlySaleProfitHistory

admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Model)
admin.site.register(ProductQuantityHistory)
admin.site.register(MonthlySaleProfitHistory)