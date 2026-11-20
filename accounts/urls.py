from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('farmer-dashboard/', views.farmer_dashboard,
         name='farmer_dashboard'),
    path('admin-dashboard/', views.admin_dashboard,
         name='admin_dashboard'),
]