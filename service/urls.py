from django.urls import path
from .import views 

urlpatterns = [
    
    path('add_service/', views.add_service, name='add-service'),
    path('service_info/', views.service_info, name='service-info'),
]