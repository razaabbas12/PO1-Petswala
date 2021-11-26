from django.urls import path
from .views import *

urlpatterns=[
    path('', marketplace, name='marketplace'),
    path('product/<int:id>', product, name='marketplace-product')
    
]