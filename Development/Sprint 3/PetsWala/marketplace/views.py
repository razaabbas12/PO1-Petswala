from django.shortcuts import render
from .models import Product

# Create your views here.


def marketplace(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request,'marketplace/marketplace.html',context)


def search_marketplace(request):
    if request.method == "POST":
        searched = request.POST['searched']
        products = Product.objects.filter(title__contains=searched)

        return render(request, 'marketplace/search_marketplace.html', {'searched':searched, 'products':products})
    else:
        return render(request, 'marketplace/search_marketplace.html')

    return render(request, 'marketplace/search_marketplace.html')

def product(request, id=0):
    product = {}
    search = Product.objects.filter(id=id)
    isFound = (len(search)==1)
    if isFound:
        product = search[0]
        
    products = Product.objects.exclude(id=id)[:4]
    context = {
        'product' : product,
        'found' : isFound,
        'products' : products
    }
    return render(request, 'marketplace/detail.html',context)