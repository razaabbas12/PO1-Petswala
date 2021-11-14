from django.shortcuts import render
from .models import Product

# Create your views here.

def marketplace(request):
    data = Product.objects.all()
    mkt = {
        "products": data
    }

    return render(request, 'marketplace/marketplace.html', mkt)