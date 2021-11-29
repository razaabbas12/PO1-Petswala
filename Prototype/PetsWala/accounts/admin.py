from django.contrib import admin
from .models import User, Vendor, Profile

# Register your models here.

admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Profile)