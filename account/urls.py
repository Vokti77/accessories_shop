from django.urls import path
from account import views

app_name = 'account'
urlpatterns = [
    path('login/', views.userlogin, name='login'),
    path('register/', views.register, name='register'),
    # path('logout/', views.logout, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]