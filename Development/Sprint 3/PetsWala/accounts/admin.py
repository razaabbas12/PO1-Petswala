from django.contrib import admin, messages
from .models import RescueServices, ServiceProvider, User, Vendor, Profile, Vet, Review_acc, Report, Vet_appointment
from .email_service import send_service_provider_approved_email,send_rescue_service_approved_email, send_vets_approved_email

# Register your models here.

admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Profile)
admin.site.register(Review_acc)
admin.site.register(Vet_appointment)

# Service Provider Admin Actions
@admin.action(description='Approve Selected Service Providers')
def approved_service_prov(modeladmin, request, queryset):
  for service_provider in queryset:
    if service_provider.is_approved:
      messages.error(request, f"{service_provider.user.username} is already approved.")
      continue
    
    service_provider.is_approved = True
    service_provider.save()
    
    sent = send_service_provider_approved_email(service_provider.user.email)
    
    if sent:
      messages.info(request, f"{service_provider.user.username} approved and email sent.")
    else:
      messages.error(request, f"{service_provider.user.username} approved but email delivery failed.")
    
# Rescue Service Admin Actions
@admin.action(description='Approve Selected Rescue Services')
def approved_rescue_service(modeladmin, request, queryset):
  for rescue_provider in queryset:
    if rescue_provider.is_approved:
      messages.error(request, f"{rescue_provider.user.username} is already approved.")
      continue
    
    rescue_provider.is_approved = True
    rescue_provider.save()
    
    sent = send_rescue_service_approved_email(rescue_provider.user.email)
    
    if sent:
      messages.info(request, f"{rescue_provider.user.username} approved and email sent.")
    else:
      messages.error(request, f"{rescue_provider.user.username} approved but email delivery failed.")
    
@admin.action(description='Approve Selected Vets')
def approved_vet(modeladmin, request, queryset):
  for vet in queryset:
    if vet.is_approved:
      messages.error(request, f"{vet.user.username} is already approved.")
      continue
    
    vet.is_approved = True
    vet.save()
    
    sent = send_vets_approved_email(vet.user.email)
    
    if sent:
      messages.info(request, f"{vet.user.username} approved and email sent.")
    else:
      messages.error(request, f"{vet.user.username} approved but email delivery failed.")
    


class ServiceProviderAdmin(admin.ModelAdmin):
  list_display = ['user', 'is_approved', 'service_information']
  ordering = ['user']
  actions = [approved_service_prov]

admin.site.register(ServiceProvider, ServiceProviderAdmin)

class RescueServiceAdmin(admin.ModelAdmin):
  list_display = ['user', 'is_approved', 'service_information']
  ordering = ['user']
  actions = [approved_rescue_service]

admin.site.register(RescueServices, RescueServiceAdmin)

class VetAdmin(admin.ModelAdmin):
  list_display = ['user', 'is_approved', 'experience']
  ordering = ['user']
  actions = [approved_vet]

admin.site.register(Vet, VetAdmin)


class ReportAdmin(admin.ModelAdmin):
  list_display = ['id', 'reported', 'title', 'role']
  ordering = ['-id']

admin.site.register(Report, ReportAdmin)