from django.urls import path
from . import views

urlpatterns=[
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),    
    path('profile/', views.profile, name='profile'),
    path('service_profile/<int:id>', views.getservprofile, name='service_profile'),
    path('resque_profile/<int:id>', views.getResqProfile, name='resque_profile'),
    path('vet_profile/<int:id>', views.getVetProfile, name='vet_profile'),
    path('vet_appointment/<int:id>', views.getVetAppointment, name='vet_appointment'),
    path('sp_appointment/<int:id>', views.getServiceAppointment, name='sp_appointment'),
    path('add_product/', views.add_product.as_view(), name='add_product'),
    path('user_register/', views.user_register.as_view(), name='user_register'),
    path('vendor_register/', views.vendor_register.as_view(), name='vendor_register'),
    path('service_provider/', views.service_provider.as_view(), name='service_provider'),    
    path('awaiting_confirmation/',views.awaiting_confirmation, name='awaiting_confirmation'),
    path('service_providers/list/',views.getServiceProviders, name='service_providers_list'),
    path('rescue_provider',views.rescue_provider.as_view(), name='rescue_providers'),
    path('rescue_providers/list/',views.getRescueProviders, name='rescue_providers_list'),
    path('vets',views.vets.as_view(), name='vets'),
    path('vets/list/',views.getVets, name='vets_list'),
    path('vets/appointments/list',views.getVetAppointmentList, name='vets_appointment_list'),
    path('vets/appointments/list/success',views.getVetAppointmentList, name='vets_appointment_list_success'),
    path('service_providers/appointments/list',views.getServiceAppointmentList, name='sp_appointment_list'),
    path('review/', views.Review_rate, name='review-rate'),
    path('report/<int:reported_id>', views.report_view, name="reports"),
    path('request/rescue/<int:requested_id>', views.request_rescue, name="request-rescue"),
    path('request/rescue/list', views.getRescueRequests, name="request-rescue-list"),
    path('rescue/detail/<int:res_id>', views.getRescueDetail, name='rescue-details'),
    path('requested/rescue/list', views.getRequestedRescue, name='requested-rescue-list'),
    path('requested/rescue/detail/<int:res_id>', views.getRequestedDetail, name='requested-rescue-details'),

]