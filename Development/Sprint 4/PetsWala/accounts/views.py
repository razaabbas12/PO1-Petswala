from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail

from marketplace.models import Product
from .models import *
from .form import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin


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
        image = request.FILES.get('image')
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        prof = Profile.objects.filter(user=request.user).first()
        if prof:
            prof.image = image if image else prof.image
            prof.save()
        
        add_form = None
        if request.user.is_serviceprovider:
            serv = ServiceProvider.objects.get(user=request.user)
            add_form = ServiceUpdateForm(instance=serv)
        elif request.user.is_rescue_service:
            resuce = RescueServices.objects.get(user=request.user)
            add_form = RescueUpdateForm(instance=resuce)
        elif request.user.is_vet:
            vet = Vet.objects.get(user=request.user)
            add_form = VetUpdateForm(instance=vet)
            
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
            serv = ServiceProvider.objects.get(user=request.user)
            add_form = ServiceUpdateForm(instance=serv)
        elif request.user.is_rescue_service:
            resuce = RescueServices.objects.get(user=request.user)
            add_form = RescueUpdateForm(instance=resuce)
        elif request.user.is_vet:
            vet = Vet.objects.get(user=request.user)
            add_form = VetUpdateForm(instance=vet)
        

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
        service_providers = ServiceProvider.objects.filter(is_approved=True, user__is_serviceprovider=True).all()
        
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

        appointment = Service_appointment.objects.get(user=service_provider)
        
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
            context["appointment"] = appointment
        else:
            context['exist'] = False
    else:
        
        context['exist']=False
        
    return render(request,'accounts/service_profile.html',context)
        

    

def getRescueProviders(request):
    if request.method == 'GET':
        rescue_providers = RescueServices.objects.filter(is_approved=True, user__is_rescue_service=True).all()
                
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
                    "profile_url" : f"/accounts/resque_profile/{provider.user.id}",
                    "uid" : provider.user.id,
                    
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
                profile = Profile.objects.filter(user=vet.user, user__is_vet=True).first()
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

        appointment = Vet_appointment.objects.get(user=vet)
        
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
            context["appointment"] = appointment
        else:
            context['exist'] = False
    else:
        
        context['exist']=False
        
    return render(request,'accounts/vet_profile.html',context)
        
        
def getVetAppointment(request, id):

    user =User.objects.filter(id=id).first()
    vet = Vet.objects.filter(user=user).first()
    vet_app = Vet_appointment.objects.filter(user=vet)

    if request.method == "POST":
        your_name = request.POST['your-name']
        your_phone = request.POST['your-phone']
        your_email = request.POST['your-email']
        your_address = request.POST['your-address']
        your_schedule = request.POST.get("a")
        your_message = request.POST['your-message']
        your_vet = user.username

        if your_schedule=="m1":
            vet_app.update(m1=True)  
            your_name = "WORKING m1"
            appointment = "Name : " + your_name + "Phone : " + your_phone + "Email : " + your_email + "Address: " + your_address + "Time: " + your_schedule + "Day: " + "Message : " + your_message

        elif your_schedule=="m2":
            vet_app.update(m2=True)
            your_name = "WORKING m2"
        
        elif your_schedule=="m3":
            vet_app.update(m3=True)
            your_name = "WORKING m3"

        elif your_schedule=="m4":
            vet_app.update(m4=True)
            your_name = "WORKING m4"

        elif your_schedule=="t1":
            vet_app.update(t1=True)  
            your_name = "WORKING t1"
            appointment = "Name : " + your_name + "Phone : " + your_phone + "Email : " + your_email + "Address: " + your_address + "Time: " + your_schedule + "Day: " + "Message : " + your_message

        elif your_schedule=="t2":
            vet_app.update(t2=True)
            your_name = "WORKING t2"
        
        elif your_schedule=="t3":
            vet_app.update(t3=True)
            your_name = "WORKING t3"

        elif your_schedule=="t4":
            vet_app.update(t4=True)
            your_name = "WORKING t4"

        elif your_schedule=="w1":
            vet_app.update(w1=True)  
            your_name = "WORKING w1"
            appointment = "Name : " + your_name + "Phone : " + your_phone + "Email : " + your_email + "Address: " + your_address + "Time: " + your_schedule + "Day: " + "Message : " + your_message

        elif your_schedule=="w2":
            vet_app.update(w2=True)
            your_name = "WORKING w2"
        
        elif your_schedule=="w3":
            vet_app.update(w3=True)
            your_name = "WORKING w3"

        elif your_schedule=="w4":
            vet_app.update(w4=True)
            your_name = "WORKING w4"

        elif your_schedule=="th1":
            vet_app.update(th1=True)  
            your_name = "WORKING th1"
            appointment = "Name : " + your_name + "Phone : " + your_phone + "Email : " + your_email + "Address: " + your_address + "Time: " + your_schedule + "Day: " + "Message : " + your_message

        elif your_schedule=="th2":
            vet_app.update(th2=True)
            your_name = "WORKING th2"
        
        elif your_schedule=="th3":
            vet_app.update(th3=True)
            your_name = "WORKING th3"

        elif your_schedule=="th4":
            vet_app.update(th4=True)
            your_name = "WORKING th4"

        elif your_schedule=="f1":
            vet_app.update(f1=True)  
            your_name = "WORKING f1"
            appointment = "Name : " + your_name + "Phone : " + your_phone + "Email : " + your_email + "Address: " + your_address + "Time: " + your_schedule + "Day: " + "Message : " + your_message

        elif your_schedule=="f2":
            vet_app.update(f2=True)
            your_name = "WORKING f2"
        
        elif your_schedule=="f3":
            vet_app.update(f3=True)
            your_name = "WORKING f3"

        elif your_schedule=="f4":
            vet_app.update(f4=True)
            your_name = "WORKING f4"

        else:
            appointment = "NOT WORKING"
            your_name = "NOT WORKING"
            


        
        # send_mail(
        #     'Appointment Request',
        #     appointment,
        #     your_email,
        #     user.email,
        # )

        return render(request, 'accounts/vet_appointment.html', {
            'your_name': your_name,
            'your_phone' : your_phone,
            'your_email' : your_email,
            'your_address' : your_address,
            'your_schedule' : your_schedule,
            'your_message' : your_message,
            'your_vet' : your_vet
        })

def getVetAppointmentList(request):
    if request.method == 'GET':

        user = request.user
        vet = Vet.objects.get(user=user)

        vet_appointments = Vet_appointment.objects.get(user=vet)

        context = {
            "is_vet": user.is_vet,
            "vet_appointments": vet_appointments
        }

        return render(request, 'accounts/vet_appointment_list.html', context)

    if request.method == 'POST':
        user = request.user
        vet = Vet.objects.get(user=user)
        vet_app = Vet_appointment.objects.filter(user=vet)

        a_s = request.POST.get("as")
        if a_s=="m1":
            vet_app.update(m1=False)  
        
        elif a_s=="m2":
            vet_app.update(m2=False)
            
        elif a_s=="m3":
            vet_app.update(m3=False)
            
        elif a_s=="m4":
            vet_app.update(m4=False)

        elif a_s=="t1":
            vet_app.update(t1=False)  
            
        elif a_s=="t2":
            vet_app.update(t2=False)
            
        elif a_s=="t3":
            vet_app.update(t3=False)
            
        elif a_s=="t4":
            vet_app.update(t4=False)
            
        elif a_s=="w1":
            vet_app.update(w1=False)  
            
        elif a_s=="w2":
            vet_app.update(w2=False)
            
        elif a_s=="w3":
            vet_app.update(w3=False)
            
        elif a_s=="w4":
            vet_app.update(w4=False)
            
        elif a_s=="th1":
            vet_app.update(th1=False)  
            
        elif a_s=="th2":
            vet_app.update(th2=False)
            
        elif a_s=="th3":
            vet_app.update(th3=False)
           
        elif a_s=="th4":
            vet_app.update(th4=False)
            
        elif a_s=="f1":
            vet_app.update(f1=False)  
            
        elif a_s=="f2":
            vet_app.update(f2=False)
            
        elif a_s=="f3":
            vet_app.update(f3=False)
            
        elif a_s=="f4":
            vet_app.update(f4=False)
        else:
            appointment = "NOT WORKING"
            your_name = "NOT WORKING"

        context = {
            "is_vet": user.is_vet,
            "vet_appointments": vet_app
        }

        return render(request, 'accounts/vet_appointment_list_success.html', context)
        





def getServiceAppointment(request, id):

    user =User.objects.filter(id=id).first()
    sp = ServiceProvider.objects.filter(user=user).first()
    sp_app = Service_appointment.objects.filter(user=sp)

    if request.method == "POST":
        your_name = request.POST['your-name']
        your_phone = request.POST['your-phone']
        your_email = request.POST['your-email']
        your_address = request.POST['your-address']
        your_schedule = request.POST.get("a")
        your_message = request.POST['your-message']
        your_sp = user.username

        if your_schedule=="m1":
            sp_app.update(m1=True)  
            your_name = "WORKING m1"
            appointment = "Name : " + your_name + "Phone : " + your_phone + "Email : " + your_email + "Address: " + your_address + "Time: " + your_schedule + "Day: " + "Message : " + your_message

        elif your_schedule=="m2":
            sp_app.update(m2=True)
            your_name = "WORKING m2"
        
        elif your_schedule=="m3":
            sp_app.update(m3=True)
            your_name = "WORKING m3"

        elif your_schedule=="m4":
            sp_app.update(m4=True)
            your_name = "WORKING m4"

        elif your_schedule=="t1":
            sp_app.update(t1=True)  
            your_name = "WORKING t1"
            appointment = "Name : " + your_name + "Phone : " + your_phone + "Email : " + your_email + "Address: " + your_address + "Time: " + your_schedule + "Day: " + "Message : " + your_message

        elif your_schedule=="t2":
            sp_app.update(t2=True)
            your_name = "WORKING t2"
        
        elif your_schedule=="t3":
            sp_app.update(t3=True)
            your_name = "WORKING t3"

        elif your_schedule=="t4":
            sp_app.update(t4=True)
            your_name = "WORKING t4"

        elif your_schedule=="w1":
            sp_app.update(w1=True)  
            your_name = "WORKING w1"
            appointment = "Name : " + your_name + "Phone : " + your_phone + "Email : " + your_email + "Address: " + your_address + "Time: " + your_schedule + "Day: " + "Message : " + your_message

        elif your_schedule=="w2":
            sp_app.update(w2=True)
            your_name = "WORKING w2"
        
        elif your_schedule=="w3":
            sp_app.update(w3=True)
            your_name = "WORKING w3"

        elif your_schedule=="w4":
            sp_app.update(w4=True)
            your_name = "WORKING w4"

        elif your_schedule=="th1":
            sp_app.update(th1=True)  
            your_name = "WORKING th1"
            appointment = "Name : " + your_name + "Phone : " + your_phone + "Email : " + your_email + "Address: " + your_address + "Time: " + your_schedule + "Day: " + "Message : " + your_message

        elif your_schedule=="th2":
            sp_app.update(th2=True)
            your_name = "WORKING th2"
        
        elif your_schedule=="th3":
            sp_app.update(th3=True)
            your_name = "WORKING th3"

        elif your_schedule=="th4":
            sp_app.update(th4=True)
            your_name = "WORKING th4"

        elif your_schedule=="f1":
            sp_app.update(f1=True)  
            your_name = "WORKING f1"
            appointment = "Name : " + your_name + "Phone : " + your_phone + "Email : " + your_email + "Address: " + your_address + "Time: " + your_schedule + "Day: " + "Message : " + your_message

        elif your_schedule=="f2":
            sp_app.update(f2=True)
            your_name = "WORKING f2"
        
        elif your_schedule=="f3":
            sp_app.update(f3=True)
            your_name = "WORKING f3"

        elif your_schedule=="f4":
            sp_app.update(f4=True)
            your_name = "WORKING f4"

        else:
            appointment = "NOT WORKING"
            your_name = "NOT WORKING"
            


        
        # send_mail(
        #     'Appointment Request',
        #     appointment,
        #     your_email,
        #     user.email,
        # )

        return render(request, 'accounts/sp_appointment.html', {
            'your_name': your_name,
            'your_phone' : your_phone,
            'your_email' : your_email,
            'your_address' : your_address,
            'your_schedule' : your_schedule,
            'your_message' : your_message,
            'your_vet' : your_sp
        })

def getServiceAppointmentList(request):
    if request.method == 'GET':

        user = request.user
        sp = ServiceProvider.objects.get(user=user)

        sp_appointments = Service_appointment.objects.get(user=sp)

        context = {
            "is_serviceprovider": user.is_serviceprovider,
            "sp_appointments": sp_appointments
        }

        return render(request, 'accounts/sp_appointment_list.html', context)



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
    
def report_view(request, reported_id):
    if request.method=="GET":
        ted_user = User.objects.get(id=reported_id)
        
        context = {
            "reported": reported_id,
            "name": f"{ted_user.first_name} {ted_user.last_name}",
            "form": ReportForm,
            "link": whoamilink(ted_user),
            "role": whoami(ted_user)
        }
        
        return render(request,'accounts/report_init.html', context)
    elif request.method=="POST":
        tee_user = request.user
        ted_user = User.objects.get(id=reported_id)
        ted_prof = Profile.objects.get(user=ted_user)
        data = request.POST
        
        title=data.get('title')
        desc=data.get('description')
        image = request.FILES.get('image')
        role=whoami(ted_user)
        rep = Report(user=tee_user, reported=ted_prof, title=title, description=desc,image=image,role=role)
        rep.save()
        context = {
            "rep_id": rep.id
        }
        return render(request,'accounts/report_recived.html',context)

@csrf_exempt
def request_rescue(request, requested_id):
    if request.method=="GET":
        ted_user = User.objects.get(id=requested_id)
        
        context = {
            
            "requested": requested_id,
            "name": f"{ted_user.first_name} {ted_user.last_name}",
            "form": RequestForm,
            "link": whoamilink(ted_user)
        }
        return render(request,'accounts/request_rescue.html', context)
    
    elif request.method=="POST":
        data = request.POST
        address = data.get("address", None)
        lat = data.get("lat", None)
        lng = data.get("lng", None)
        
        if not address or not lat or not lng:
            return render(request,'accounts/address_required.html',{})
        
        ad = Address(address=address, lat=lat, lng=lng)
        ad.save()
        
        tee_user = request.user
        ted_user = User.objects.get(id=requested_id)
        ted_prof = Profile.objects.get(user=ted_user)
        
        title=data.get('title')
        desc=data.get('description')  
        img = request.FILES.get('image')
        
        req = Request(user=tee_user, requested=ted_prof, title=title, description=desc,address=ad)
        req.image = img
        
        req.save()
        
        return render(request,'accounts/request_recv.html',{"id":req.id})
    
def getRescueRequests(request):
    if request.method == 'GET':
        user= request.user
        
        prof = Profile.objects.get(user=user)
        requests = Request.objects.filter(requested=prof).all()
        
        context = {
            "is_rescue" : user.is_rescue_service,
            "requests": requests
        }
        return render(request,'accounts/request_list.html',context)
    
def getRescueDetail(request, res_id):
    if request.method == 'GET':
        req = Request.objects.filter(id=res_id).first()
    
    elif request.method == 'POST':
        data = request.POST
        
        status = data.get('status')
        rescue_note = data.get('rescue_note')
        resc_addr_lat = data.get('resc_addr_lat')
        resc_addr_lng = data.get('resc_addr_lng')
        print(data)
        req = Request.objects.filter(id=res_id).first()
        if req:
            req.status = status if status else req.status
            req.rescue_note = rescue_note if rescue_note else req.rescue_note
            req.resc_addr_lat = resc_addr_lat if resc_addr_lat else req.resc_addr_lat
            req.resc_addr_lng = resc_addr_lng if resc_addr_lng else req.resc_addr_lng
            req.save()
    
    user = request.user
    r_form = RequestRecuerForm(instance=req)
    exists = bool(req) 
    context = {
        "is_rescue" : user.is_rescue_service,
        "req": req,
        "exist": exists,
        "r_form": r_form
    }
    return render(request,'accounts/rescue_detail.html',context)

def getRequestedRescue(request):
    if request.method == 'GET':
        user= request.user
        
        requests = Request.objects.filter(user=user).all()
        
        context = {
            "requests": requests
        }
        return render(request,'accounts/requested_rescue_list.html',context)
    
def getRequestedDetail(request, res_id):
    if request.method == 'GET':
        req = Request.objects.filter(id=res_id).first()    
        exists = bool(req) 
        context = {
            "req": req,
            "exist": exists
        }
        return render(request,'accounts/requested_res_detail.html',context)
    

