from django.urls import path
from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('dashboard', views.index, name='dashboard'),
    path('add_brand/', views.add_brand, name='add-brand'),
    path('add_product/', views.add_product, name='add-product'),
    path('upadate_product/<int:product_id>/', views.upadate_product, name='upadate-product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete-product'),
    path('Sale_quantity/<int:product_id>/', views.sale_quantity, name='Sale-quantity'),
    path('confirm_Sale/<int:product_id>/', views.confirm_Sale, name='confirm-Sale'),
    path('product_csv/', views.product_csv, name='product-csv'),
    path('calculate_profit/', views.calculate_profit, name='calculate-profit'),
    path('report/<str:type>/', views.report, name='report'),
    path('daily_report/', views.daily_report, name='daily-report'),
    
    path('accessories_summary/', views.accessories_summary,name="accessories_summary"),
    path('stats/', views.stats_view,name="stats"),
    path('summary/', views.summary,name="summary"),
    path('filter/', views.filter_data,name="filter"),


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
    path("chat/", views.chat, name="chat"),

]