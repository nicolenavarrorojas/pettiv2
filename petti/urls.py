"""
URL configuration for petti project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views 
from app import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), 
    path('register/', views.register, name='register'),
    path('services/', views.services, name='services'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create-reservation/<int:service_id>', views.create_reservation, name='create_reservation'),
    path('create-reservation-and-payment/<int:service_id>', views.create_reservation_and_payment, name='create_reservation_and_payment'),
    path('payment-success/<int:reservation_id>', views.payment_success, name='payment_success'),
    path('logout/', views.logout_view, name='logout'),

    path('add-service/', views.add_service, name='add_service'),
    path('client-profile/', views.client_profile, name='client_profile'),
    path('partner-profile-form/', views.partner_profile_form, name='partner_profile_form'),
    path('partner-profile/', views.partner_profile, name='partner_profile'),
    path('partner-public-view/', views.partner_public_view, name='partner_public_view'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
