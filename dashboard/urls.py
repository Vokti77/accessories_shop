from django.urls import path
from dashboard import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

app_name = 'dashboard'
urlpatterns = [
    path('redirect-admin/', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('dashboard', views.index, name='dashboard'),

    path('add_brand/', views.add_brand, name='add-brand'),
    path('upadate_brand/<int:brand_id>/', views.upadate_brand, name='upadate-brand'),
    path('delete_brand/<int:brand_id>/', views.delete_brand, name='delete-brand'),

    path('add_model/', views.add_model, name='add-model'),
    path('upadate_model/<int:model_id>/', views.upadate_model, name='update-model'),

    path('add_product/', views.add_product, name='add-product'),
    path('get_models/', views.get_models, name='get_models'),
    path('upadate_product/<int:product_id>/', views.upadate_product, name='upadate-product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete-product'),

    path('Sale_quantity/<int:product_id>/', views.sale_quantity, name='Sale-quantity'),
    path('confirm_Sale/<int:product_id>/', views.confirm_Sale, name='confirm-Sale'),
    path('report/', views.report, name='report'),
 
    path('update_product_quantity/<int:product_id>/', views.update_product_quantity, name='update-quantity'),
    path('confirm_update_quantity/<int:product_id>/', views.confirm_update_quantity, name='update-confirm'),
    path('update_quntity_history/', views.update_quntity_history, name='update-history'),

    path("statistics/", views.statistics_view, name="shop-statistics"),
    path("filter-options/", views.get_filter_options, name="chart-filter-options"),
    path("sales/<int:year>/", views.get_sales_chart, name="chart-sales"),
    path("spend-per-customer/<int:year>/", views.spend_per_customer_chart, name="chart-spend-per-customer"),

    path("charts/", views.charts, name="charts"),
    path("widgets/", views.widgets, name="widgets"),
    path("tables/", views.tables, name="tables"),
    path("grid/", views.grid, name="grid"),
    path("form-basic/", views.form_basic, name="form-basic"),
    path("form-wizard/", views.form_wizard, name="form-wizard"),
    path("buttons/", views.buttons, name="buttons"),
    path("icon-material/", views.icon_material, name="icon-material"),
    path("icon-fontawesome/", views.icon_fontawesome, name="icon-fontawesome"),
    path("elements/", views.elements, name="elements"),
    path("gallery/", views.gallery, name="gallery"),
    path("invoice/", views.invoice, name="invoice"),
   
]