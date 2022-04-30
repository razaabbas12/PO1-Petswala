from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from django.forms import widgets

from blog.models import Post
from .models import *
from marketplace.models import Category, Product


# class UserAddressForm(forms.ModelForm):
#     class Meta:
#         model  = UserAddress
#         exclude = ('user','shipping',)

class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    city = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.address = self.cleaned_data.get('address')
        user.city = self.cleaned_data.get('city')
        user.save()
        return user


class VendorSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(required=True)
    product_category = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    service_information = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.save()
        vendor = Vendor.objects.create(user=user)
        vendor.address = self.cleaned_data.get('address')
        user.is_vendor = True
        vendor.product_category = self.cleaned_data.get('product_category')
        vendor.save()
        vendor.service_information = self.cleaned_data.get('service_information')
        vendor.save()
        return user

class ServiceSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(required=True)
    service_information = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        
        user.is_vendor = False
        user.is_serviceprovider = True
        user.is_rescue_service = False
        user.is_vet= False
        
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.save()
        
        service = ServiceProvider.objects.create(user=user)
        service.service_information = self.cleaned_data.get('service_information')
        service.is_approved = False
        service.save()
        
        return service

class RescueSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(required=True)
    service_information = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        
        user.is_vendor = False
        user.is_serviceprovider = False
        user.is_rescue_service = True
        user.is_vet= False
        
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.save()
        
        rescue = RescueServices.objects.create(user=user)
        rescue.service_information = self.cleaned_data.get('service_information')
        rescue.is_approved = False
        rescue.save()
        
        return user

class VetsSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(required=True)
    experience = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        
        user.is_vendor = False
        user.is_serviceprovider = False
        user.is_rescue_service = False
        user.is_vet = True      
        
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.save()
        
        vet = Vet.objects.create(user=user)
        vet.experience = self.cleaned_data.get('experience')
        vet.is_approved = False
        vet.save()
        
        return vet

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','phone_number','email', 'address']

class VendorUpadteForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['address','product_category','service_information']
        
class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['address','service_information']

class RescueUpdateForm(forms.ModelForm):
    class Meta:
        model = RescueServices
        fields = ['address','service_information']

class VetUpdateForm(forms.ModelForm):
    class Meta:
        model = Vet
        fields = ['address','experience']
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title','description','image']

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title','description','image']
        
class RequestRecuerForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['status','rescue_note']


class AddNewProduct(forms.ModelForm):         #Implement add_product form here
    # category = forms.Select()
    # vendor = forms.Select()                   #Fix vendor definition in product model
    # title = forms.CharField(required=True)
    # slug = forms.CharField(required=True)
    # description = forms.CharField(required=True)
    # price = forms.DecimalField(required=True)
    # image = forms.ImageField(required=True)
    # thumbnail = forms.ImageField(required=True)

    class Meta:
        model = Product
        fields = ['title', 'slug','category', 'description', 'price', 'image', 'thumbnail']

        widgets={
            'title': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Product Title here..."
            }),
            'slug': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Unique Slug here..."
            }),
            'category': forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Enter Product Category here..."
            }),
             'vendor': forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Enter Product Category here..."
            }),
            'description': forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter Product Description here...",
                "rows": 4
            }),
            'price': forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Price"
            }),
            'image': forms.ClearableFileInput(attrs={
                "class": "form-control",
                "required": True
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),

        }

    @transaction.atomic
    def save(self):
        product = super().save(commit=False)
        product.title = self.cleaned_data.get('title')
        product.slug = self.cleaned_data.get('slug')
        product.category = self.cleaned_data.get('category')
        product.description = self.cleaned_data.get('description')
        vendor = Vendor.objects.filter(user=self.instance.user).first()
        product.vendor = vendor
        product.price = self.cleaned_data.get('price')
        product.image = self.cleaned_data.get('image')
        product.thumbnail = self.cleaned_data.get('thumbnail')
        product.save()
        return product
