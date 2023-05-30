from django.urls import path
from .views import monthly_sale_profit_view
from accessories import views


urlpatterns = [
    # Other URL patterns
    path('monthly-sale-profit/', views.monthly_sale_profit_view, name='monthly_sale_profit'),
]