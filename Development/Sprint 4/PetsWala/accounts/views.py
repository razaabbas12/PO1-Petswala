from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from django.views.generic import CreateView
from django.urls import reverse_lazy

from marketplace.models import Product
from .models import ServiceProvider, User, Vendor, RescueServices, Vet, Review_acc, Profile, Report
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
        add_form=None
        if request.user.is_serviceprovider:
            add_form = ServiceUpdateForm(request.POST, instance=request.user.serviceprovider)
        elif request.user.is_rescue_service:
            add_form = RescueUpdateForm(request.POST, instance=request.user.rescueservice)
        elif request.user.is_vet:
            add_form = VetUpdateForm(request.POST, instance=request.user.vet)
        else:
            pass
            
        if u_form.is_valid() or p_form.is_valid():
            u_form.save()
            p_form.save()
            if add_form:
                if add_form.is_valid():
                    add_form.save()
            messages.success(request, f'Your Profile Information Has Been Updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        add_form = None
        if request.user.is_serviceprovider:
            add_form = ServiceUpdateForm(instance=request.user.serviceprovider)
        elif request.user.is_rescue_service:
            add_form = RescueUpdateForm(instance=request.user.rescueservice)
        elif request.user.is_vet:
            add_form = VetUpdateForm(instance=request.user.vet)
        

    prof = Profile.objects.filter(user=request.user).first()
    user_ = request.user
    profreview =Profile.objects.get(user=user_)
    review = Review_acc.objects.filter(profile=profreview).all()
    
    reviews = []
    for one in review:
        temp = {
            "rate": list(range(one.rate)),
            "comment": one.comment,
            "name": f"{one.user.username}",
            "time": one.created_at.strftime("%d %b %Y %H:%M")
        }
        prof = Profile.objects.filter(user=one.user).first()
        temp["image"] = prof.image.url
        reviews.append(temp)
        
    
    whoami = ""
    info = ""
    
    if user_.is_vendor:
        vendor = Vendor.objects.filter(user=user_).first()
        whoami = "Vendor"
        info = vendor.service_information
    elif user_.is_serviceprovider:
        prodvider = ServiceProvider.objects.filter(user=user_).first()
        whoami = "Service Prodvider"
        info = prodvider.service_information
    elif user_.is_rescue_service:
        prodvider = RescueServices.objects.filter(user=user_).first()
        whoami = "Rescue Provider"
        info = prodvider.service_information
    elif user_.is_vet:
        vet = Vet.objects.filter(user=user_).first()
        whoami = "Vet"
        info = vet.experience
    else:
        whoami = "User"
    
    if prof:
        context = {
            "reviews" :reviews,
            'u_form': u_form,
            'p_form': p_form,
            "add_form": add_form,
            "name" : f"{user_.first_name} {user_.last_name}",
            "image": prof.image.url,
            "phone_number": user_.phone_number,
            "email": user_.email,
            "info": info,
            "whoami": whoami
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
    
class service_provider(CreateView):
    model = ServiceProvider
    form_class = ServiceSignUpForm
    template_name = 'accounts/service_provider.html'

    def form_valid(self, form):
        form.save()
        return render(self.request, 'accounts/awaiting_confirmation.html')

class rescue_provider(CreateView):
    model = RescueServices
    form_class = RescueSignUpForm
    template_name = 'accounts/rescue.html'

    def form_valid(self, form):
        form.save()
        return render(self.request, 'accounts/awaiting_confirmation.html')
  
class vets(CreateView):
    model = Vet
    form_class = VetsSignUpForm
    template_name = 'accounts/vets.html'

    def form_valid(self, form):
        form.save()
        return render(self.request, 'accounts/awaiting_confirmation.html')
     

class add_product(CreateView):
    model = Product
    form_class = AddNewProduct
    template_name = 'accounts/add_new_product.html'
    success_url = reverse_lazy('marketplace')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
def awaiting_confirmation(request):
    return render(request, 'blog/awaiting_confirmation.html')


def getServiceProviders(request):
    if request.method == 'GET':
        service_providers = ServiceProvider.objects.filter(is_approved=True).all()
        
        data = []
        for provider in service_providers:
            try:
                profile = Profile.objects.filter(user=provider.user).first()
                obj = {
                    "name" : f"{provider.user.first_name} {provider.user.last_name}",
                    "service_info" : provider.service_information[:50]+"...",
                    "phone_num" : provider.user.phone_number,
                    "image" : profile.image.url,
                    "email" : provider.user.email,
                    "profile_url" : f"/accounts/service_profile/{provider.user.id}"
                }
                
                if not provider.user.is_blocked:
                    data.append(obj)
            except:
                pass
        
        context = {
            "service_providers" : data
        }
        return render(request,'accounts/list_service.html',context)


def getservprofile(request, id):
    user =User.objects.filter(id=id).first()
    
    context = {}
    if user:
        context={
            "exist": user.is_serviceprovider
        }
        
        profile = Profile.objects.filter(user=user).first()
        service_provider = ServiceProvider.objects.filter(user=user).first()
        
        profreview =Profile.objects.get(user=user)
        review = Review_acc.objects.filter(profile=profreview).all()
        
        reviews = []
        for one in review:
            temp = {
                "rate": list(range(one.rate)),
                "comment": one.comment,
                "name": f"{one.user.username}",
                "time": one.created_at.strftime("%d %b %Y %H:%M")
            }
            profile = Profile.objects.filter(user=one.user).first()
            temp["image"] = profile.image.url
            reviews.append(temp)
          

        if profile and service_provider:
            context["name"] = f"{user.first_name} {user.last_name}"
            context["image"] = profile.image.url
            context["phone_number"] = user.phone_number
            context["email"] = user.email
            context["service_information"] = service_provider.service_information
            context["uid"] = user.id
            context["url"] = "service_profile"
            context["reviews"] = reviews
        else:
            context['exist'] = False
    else:
        
        context['exist']=False
        
    return render(request,'accounts/service_profile.html',context)
        

def getRescueProviders(request):
    if request.method == 'GET':
        rescue_providers = RescueServices.objects.filter(is_approved=True).all()
                
        data = []
        for provider in rescue_providers:
            try:
                profile = Profile.objects.filter(user=provider.user).first()
                obj = {
                    "name" : f"{provider.user.first_name} {provider.user.last_name}",
                    "service_info" : provider.service_information[:50]+"...",
                    "phone_num" : provider.user.phone_number,
                    "image" : profile.image.url,
                    "email" : provider.user.email,
                    "profile_url" : f"/accounts/resque_profile/{provider.user.id}"
                }
                
                if not provider.user.is_blocked:
                    data.append(obj)
                
            except:
                pass
        
        context = {
            "rescue_providers" : data
        }
        return render(request,'accounts/rescue_list.html',context)

def getResqProfile(request, id):
    user =User.objects.filter(id=id).first()
    
    context = {}
    if user:
        context={
            "exist": user.is_rescue_service
        }
        
        profile = Profile.objects.filter(user=user).first()
        Resque_provider = RescueServices.objects.filter(user=user).first()
        
        
        profreview =Profile.objects.get(user=user)
        review = Review_acc.objects.filter(profile=profreview).all()
        
        reviews = []
        for one in review:
            temp = {
                "rate": list(range(one.rate)),
                "comment": one.comment,
                "name": f"{one.user.username}",
                "time": one.created_at.strftime("%d %b %Y %H:%M")
            }
            profile = Profile.objects.filter(user=one.user).first()
            temp["image"] = profile.image.url
            reviews.append(temp)
            
        
        if profile and Resque_provider:
            context["name"] = f"{user.first_name} {user.last_name}"
            context["image"] = profile.image.url
            context["phone_number"] = user.phone_number
            context["email"] = user.email
            context["service_information"] = Resque_provider.service_information
            context["uid"] = user.id
            context["url"] = "resque_profile"
            context["reviews"] = reviews
        else:
            context['exist'] = False
    else:
        
        context['exist']=False
        
    return render(request,'accounts/resque_profile.html',context)
        


def getVets(request):
    if request.method == 'GET':
        vets = Vet.objects.filter(is_approved=True).all()
        
        data = []
        for vet in vets:
            try:
                profile = Profile.objects.filter(user=vet.user).first()
                obj = {
                    "name" : f"{vet.user.first_name} {vet.user.last_name}",
                    "experience" : vet.experience[:50]+"...",
                    "phone_num" : vet.user.phone_number,
                    "image" : profile.image.url,
                    "email" : vet.user.email,
                    "profile_url" : f"/accounts/vet_profile/{vet.user.id}"
                }
                
                if not vet.user.is_blocked:
                    data.append(obj)
            except:
                pass
        
        context = {
            "vets" : data
        }
        return render(request,'accounts/vets_list.html',context)
    
def getVetProfile(request, id):
    user =User.objects.filter(id=id).first()
    
    context = {}
    if user:
        context={
            "exist": user.is_vet
        }
        
        profile = Profile.objects.filter(user=user).first()
        vet = Vet.objects.filter(user=user).first()
        
        profreview =Profile.objects.get(user=user)
        review = Review_acc.objects.filter(profile=profreview).all()
        
        reviews = []
        for one in review:
            temp = {
                "rate": list(range(one.rate)),
                "comment": one.comment,
                "name": f"{one.user.username}",
                "time": one.created_at.strftime("%d %b %Y %H:%M")
            }
            profile = Profile.objects.filter(user=one.user).first()
            temp["image"] = profile.image.url
            reviews.append(temp)
        
        if profile and vet:
            context["name"] = f"{user.first_name} {user.last_name}"
            context["image"] = profile.image.url
            context["phone_number"] = user.phone_number
            context["email"] = user.email
            context["experience"] = vet.experience
            context["uid"] = user.id
            context["url"] = "vet_profile"
            context["reviews"] = reviews
        else:
            context['exist'] = False
    else:
        
        context['exist']=False
        
    return render(request,'accounts/vet_profile.html',context)
        
def Review_rate(request):
    if request.method =="POST":
        data = request.POST
        uid = data.get("uid")
        user = User.objects.get(id=uid)
        profile = Profile.objects.get(user=user)
        comment = data.get("comment")
        rate = data.get("rate")
        url = data.get("url")
        user = request.user
        Review_acc(user=user, profile=profile, comment=comment, rate=rate).save()
        return redirect(f"/accounts/{url}/{uid}")
    
def whoami(user_):
    if user_.is_vendor:
        return "Vendor"
    elif user_.is_serviceprovider:
        return "Service Prodvider"
    elif user_.is_rescue_service:
        return "Rescue Provider"
    elif user_.is_vet:
        return "Vet"
    else:
        return "User"
    
def whoamilink(user_):
    if user_.is_vendor:
        return "Vendor"
    elif user_.is_serviceprovider:
        return "service_profile"
    elif user_.is_rescue_service:
        return "resque_profile"
    elif user_.is_vet:
        return "vet_profile"
    else:
        return "User"
    
def report_view(request, repotee_id, reported_id):
    if request.method=="GET":
        ted_user = User.objects.get(id=reported_id)
        
        context = {
            "repotee": repotee_id,
            "reported": reported_id,
            "name": f"{ted_user.first_name} {ted_user.last_name}",
            "form": ReportForm,
            "link": whoamilink(ted_user),
            "role": whoami(ted_user)
        }
        
        return render(request,'accounts/report_init.html', context)
    elif request.method=="POST":
        tee_user = User.objects.get(id=repotee_id)
        ted_user = User.objects.get(id=reported_id)
        ted_prof = Profile.objects.get(user=ted_user)
        data = request.POST
        
        title=data.get('title')
        desc=data.get('description')
        image=data.get('image')
        role=whoami(ted_user)
        rep = Report(user=tee_user, reported=ted_prof, title=title, description=desc,image=image,role=role)
        rep.save()
        context = {
            "rep_id": rep.id
        }
        return render(request,'accounts/report_recived.html',context)
    
def request_rescue(request, requestee_id, requested_id):
    if request.method=="GET":
        ted_user = User.objects.get(id=requested_id)
        
        context = {
            "requestee": requestee_id,
            "requested": requested_id,
            "name": f"{ted_user.first_name} {ted_user.last_name}",
            "form": RequestForm,
            "link": whoamilink(ted_user)
        }
        return render(request,'accounts/request_rescue.html', context)
    
    elif request.method=="POST":
        tee_user = User.objects.get(id=requestee_id)
        ted_user = User.objects.get(id=requested_id)
        ted_prof = Profile.objects.get(user=ted_user)
        data = request.POST
        
        title=data.get('title')
        desc=data.get('description')
        address=data.get('address')
        req = Request(user=tee_user, requested=ted_prof, title=title, description=desc,address=address) 
        req.save()
        context = {
            "req_id": req.id
        }
        return render(request,'accounts/request_recv.html',context)