from urllib.request import Request
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, Http404
from .models import *
from .utils import id_generator
from django.contrib import messages
from accounts.models import Profile, User, UserAddress 
# from accounts.form import UserAddressForm
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
    cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product, vendor = product.vendor.user.username, user = request.user, cartID = cart.id)
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
        # cart.active = True
        # new_cart = Cart()
        # request.session['cart_id'] = new_cart.id
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.address = request.user.address
        new_order.city = request.user.city
        new_order.order_id = id_generator()
        new_order.sub_total = cart.total
        new_order.placed = True
        # new_order.final_total = cart.total
        new_order.save()
    except:
        return HttpResponseRedirect(reverse('cart'))

    # obj = get_object_or_404(UserAddress, user = request.user)
    # try:
    #     address_form = UserAddressForm(request.POST or None, instance=request.user.useraddress)
    # except UserAddress.DoesNotExist:
    #     new_address = UserAddress()
    #     new_address.user = request.user
    #     new_address.save()
    #     address_form = UserAddressForm(request.POST or None, instance=request.user.useraddress)
    # # once the user finishes the payment(find commented code below)
    # # new_order.status = "Finished"
    # # new.order.save()
    for order_item in new_order.cart.cartitem_set.all():
        print(order_item.quantity)
    if new_order.status == "Finished":
        cart.delete()
        del request.session["cart_id"]
        del request.session["items_total"]
        return HttpResponseRedirect(reverse('cart'))

    context = {'new_order':new_order}
    template = 'marketplace/checkout.html'
    return render(request, template, context)


        
def order_complete(request):

    cart_id = request.session['cart_id']
    cart = Cart.objects.get(id = cart_id)
    cart.active = True
    cart.save()
    new_cart = Cart()
    request.session['cart_id'] = new_cart.id
    template = 'marketplace/order-comlete.html'
    return render(request, template, {})


def view_orders(request):
    if request.method == 'POST':
        
        u_status = request.POST.get('status')       #updated status from the form
        
        cID = request.POST.get('cartID')            #cart ID from the form, needed to specify which cart item status to change
        
        cart = Cart.objects.get(id=cID)             #getting the cart using the cart ID

        cartItems = CartItem.objects.filter(vendor=request.user.username, cart=cart)        #getting the cart item using the cart
        for object in cartItems:
            if ((u_status == "Pending") or (u_status == "Started") or (u_status == "Finished") or (u_status == "Abandoned")):       #To validate status change form input
                object.status = u_status
                object.save()
                messages.success(request, f'Order Status Has Been Updated!')
            
        

    template = 'marketplace/view_orders.html'
    carts = Cart.objects.filter(active=True)
    vendor_orders = []
    for object in carts:
        try:
            vendor_orders.append(CartItem.objects.get(vendor = request.user.username, cart=object))
        except:
            continue
    #vendor_orders = CartItem.objects.filter(vendor = request.user.username, cart=carts)
    # users = User.objects.filter(username = vendor_orders.user)
    context={
        'orders': vendor_orders,
        # 'status': 
    }
    return render(request, template, context)