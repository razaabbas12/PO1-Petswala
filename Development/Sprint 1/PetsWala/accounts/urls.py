from django.urls import path
from . import views

urlpatterns=[
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('add_product/', views.add_product.as_view(), name='add_product'),
    path('user_register/', views.user_register.as_view(), name='user_register'),
    path('vendor_register/', views.vendor_register.as_view(), name='vendor_register'),
    
]