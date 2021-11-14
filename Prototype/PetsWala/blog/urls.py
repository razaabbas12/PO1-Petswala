from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='index'),
    path('blog', views.blog, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact_us, name='blog-contact-us')
]
