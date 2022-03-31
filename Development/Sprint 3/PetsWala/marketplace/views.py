from django.shortcuts import render, redirect
from .models import Product, Review
from accounts.models import Profile, User

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

def product(request, id=0):
    search = Product.objects.filter(id=id)
    prodreview = Product.objects.get(id=id)
    review = Review.objects.filter(product=prodreview).all()
    
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
        
    isFound = (len(search)==1)
    if isFound:
        product = search[0]
        
    products = Product.objects.exclude(id=id)[:4]
    context = {
        "reviews": reviews,
        'product' : product,
        'found' : isFound,
        'products' : products
    }
    return render(request, 'marketplace/detail.html',context)

def Review_rate(request):
    if request.method =="POST":
        data = request.POST
        prod_id = data.get("prod_id")
        product = Product.objects.get(id=prod_id)
        comment = data.get("comment")
        rate = data.get("rate")
        user = request.user
        Review(user=user, product=product, comment=comment, rate=rate).save()
        return redirect(f"/marketplace/product/{prod_id}")