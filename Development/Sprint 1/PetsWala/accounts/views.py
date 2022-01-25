from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from django.views.generic import CreateView
from django.urls import reverse_lazy

from marketplace.models import Product
from .models import User, Vendor
from .form import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    return render(request, 'accounts/register.html')

# @login_required
# def add_product(request):
#     if request.method == 'POST':
#         add_form = AddNewProduct(request.POST)
#         if add_form.is_valid():
#             add_form.save()
#             messages.success(request, f'Your Product Has Been Added')
#             return redirect('profile')
#     else:
#         add_form = AddNewProduct()
#     context = {
#         'add_form' : add_form
#     }
    

    # return render(request, 'accounts/add_new_product.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile Information Has Been Updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)


class user_register(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'accounts/user_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class vendor_register(CreateView):
    model = Vendor
    form_class = VendorSignUpForm
    template_name = 'accounts/vendor_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class add_product(CreateView):
    model = Product
    form_class = AddNewProduct
    template_name = 'accounts/add_new_product.html'
    success_url = reverse_lazy('marketplace')
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)