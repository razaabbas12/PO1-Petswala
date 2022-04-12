from operator import mod
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_google_maps import fields as map_fields
# from django.db import DefaultConnectionProxy, models      #awein matlab

# Create your models here.

class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_serviceprovider = models.BooleanField(default=False)
    is_rescue_service = models.BooleanField(default=False)
    is_vet = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)

    
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(default="ABC", max_length=100)
    city = models.CharField(default="ABC", max_length=20)

class UserAddress(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    address = models.CharField(max_length = 120)
    address2 = models.CharField(max_length = 120, null = True, blank = True)
    city = models.CharField(max_length = 120, null = True, blank = True)
    state = models.CharField(max_length = 120, null = True, blank = True)
    country = models.CharField(max_length = 120, null = True, blank = True)
    zipcode = models.CharField(max_length = 25)
    phone_number = models.CharField(max_length = 25)
    shipping = models.BooleanField(default = True)
    billing = models.BooleanField(default = True)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
         verbose_name = "User Address"
         verbose_name_plural = "User Adresses"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)   #This establishes a 1-1 relationship between objects of 2 classes ie here it means 1 user can only have 1 profile and vice versa
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    # Add more fields here later. Don't forget to run migrations
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Profile'

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=100)
    product_category = models.CharField(max_length=20)
    service_information = models.TextField(default="", blank=True, null=True)
    
    def __str__(self):
        return self.user.username         #fix if problem
    
class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    service_information = models.TextField(null=True)
    
    def __str__(self):
        return self.user.username
    
class RescueServices(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    service_information = models.TextField(null=True)
    
    def __str__(self):
        return self.user.username
    
class Vet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    experience = models.TextField(null=True)
    
    def __str__(self):
        return self.user.username


class Review_acc(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    profile=models.ForeignKey(Profile,models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)



class Report(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    reported=models.ForeignKey(Profile,models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image=models.ImageField(blank=True, null=True)
    role=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.title)
    
class Address(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

class Request(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    requested=models.ForeignKey(Profile,models.CASCADE)
    address= models.ForeignKey(Address, models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image=models.ImageField(blank=True, null=True)
    role=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.title)




