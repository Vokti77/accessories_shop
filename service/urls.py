from django.urls import path
from .import views 

urlpatterns = [
    path('add_service/', views.add_service, name='add-service'),
    path('service_info/', views.service_info, name='service-info'),
    path('update_status/int<int:service_id>/', views.update_status, name='update-status'),
    path('upadate_service/<int:service_id>/', views.upadate_service, name='upadate-service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete-service'),
]