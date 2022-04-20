from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, Http404
from .models import *
from .utils import id_generator
from accounts.models import Profile, User, UserAddress 
from accounts.form import UserAddressForm
from django.contrib.auth.decorators import login_required

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

#________________
@login_required(login_url='login')
def viewCart(request):
    try:
        cart_id = request.session['cart_id']
    except:
        cart_id = None
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        context = {'cart':cart}
    else:
        empty_message = "Your cart is empty, add items to your cart..."
        context = {'empty':True, 'empty_message':empty_message}

    # cart = Cart.objects.all()[0]
    template = 'marketplace/cart.html'
    return render(request, template, context)

@login_required(login_url='login')
def update_cart(request, id):
    request.session.set_expiry(3000)
    try:
        qty = request.GET.get('qty')
        update_qty = True
    except:
        qty = ''
        update_qty = False
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
    # except Cart.DoesNotExist:
    #     cart = Cart.objects.create()
    #     request.session['cart_id'] = cart.id
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        cart_id = new_cart.id

    cart = Cart.objects.get(id = cart_id)
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        pass
    except:
        pass
    cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product)
    if created:
        print("yeah")
    if int(qty) == 0 and update_qty:
        cart_item.delete()
    elif update_qty:
        cart_item.quantity = qty
        cart_item.save()
    else:
        pass
    # if not cart_item in cart.items.all():
    #     cart.items.add(cart_item)
    # else:
    #     cart.items.remove(cart_item)
    new_total = 0.0
    for item in cart.cartitem_set.all():
        line_total = float(item.product.price) * item.quantity
        cartitem_total = line_total
        new_total += line_total
    cart_items_total = request.session['items_total'] = cart.cartitem_set.count()
    cart.total = new_total
    # queryset = CartItem.objects.filter(request.session['cart_id'])
    # print(request.session['cart_id'])
    cart.save()

    return HttpResponseRedirect(reverse('cart'))

@login_required(login_url='login')
def checkout(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
    except:
        cart_id = None
        return HttpResponseRedirect(reverse('cart'))
    try:
        new_order = Order.objects.get(cart = cart)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = id_generator()
        new_order.sub_total = cart.total
        new_order.save()
    except:
        return HttpResponseRedirect(reverse('cart'))

    # obj = get_object_or_404(UserAddress, user = request.user)
    try:
        address_form = UserAddressForm(request.POST or None, instance=request.user.useraddress)
    except UserAddress.DoesNotExist:
        new_address = UserAddress()
        new_address.user = request.user
        new_address.save()
        address_form = UserAddressForm(request.POST or None, instance=request.user.useraddress)
    # once the user finishes the payment(find commented code below)
    # new_order.status = "Finished"
    # new.order.save()
    for order_item in new_order.cart.cartitem_set.all():
        print(order_item.quantity)
    if new_order.status == "Finished":
        cart.delete()
        del request.session["cart_id"]
        del request.session["items_total"]
        return HttpResponseRedirect(reverse('cart'))

    context = {'address_form':address_form, 'new_order':new_order}
    template = 'marketplace/checkout.html'
    return render(request, template, context)

def user_add_address(request):
    try:
        redirect = request.GET.get("redirect")
    except:
        redirect = None
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        inst = UserAddress.objects.get(user = request.user)
        inst.address = request.POST.get('address')
        inst.address2 = request.POST.get('address2')
        inst.city = request.POST.get('city')
        inst.state = request.POST.get('state')
        inst.country = request.POST.get('country')
        inst.zipcode= request.POST.get('zipcode')
        inst.phone_number = request.POST.get('phone_number')
        billing = request.POST.get('billing')
        if billing == None:
            inst.billing = False
        else:
            inst.billing = True
        inst.save()
        if form.is_valid():
            form = UserAddressForm(request.POST, request.FILES, instance=request.user)
            form.save()
            if redirect is not None:
                return HttpResponseRedirect(reverse(str(redirect)))
        else:
            raise Http404