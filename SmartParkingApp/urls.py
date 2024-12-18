from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('regular-dashboard/', views.regular_dashboard, name='regular_dashboard'),
    path('guest-dashboard/', views.guest_dashboard, name='guest_dashboard'),
]
