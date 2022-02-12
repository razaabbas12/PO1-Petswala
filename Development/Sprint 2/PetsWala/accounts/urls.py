from django.urls import path
from . import views

urlpatterns=[
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('add_product/', views.add_product.as_view(), name='add_product'),
    path('user_register/', views.user_register.as_view(), name='user_register'),
    path('vendor_register/', views.vendor_register.as_view(), name='vendor_register'),
    path('service_provider/', views.service_provider.as_view(), name='service_provider'),    
    path('awaiting_confirmation/',views.awaiting_confirmation, name='awaiting_confirmation'),
    path('service_providers/list/',views.getServiceProviders, name='service_providers_list'),
    path('rescue_provider',views.rescue_provider.as_view(), name='rescue_providers'),
    path('rescue_providers/list/',views.getRescueProviders, name='rescue_providers_list'),
]