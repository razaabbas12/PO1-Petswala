from django.shortcuts import render
from .models import Post
#from django.http import HttpResponse



def home(request):
    return render(request, 'blog/index.html')

def blog(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Home',
        }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html')

def contact_us(request):
    return render(request, 'blog/contact.html')
