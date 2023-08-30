from django.shortcuts import render, redirect
from seller.models import Product
from common.models import Customer, Seller
from .models import Cart, Wishlist, Order, OrderItem
from .auth_gaurd import auth_customer
from django.db.models import Q, F
from django.http import JsonResponse, HttpResponse
import random
# from .models import Cart

# Create your views here.


@auth_customer
def master_page(request):
    return render(request, 'customer/master.html')


@auth_customer
def home_page(request):
    product_list = Product.objects.filter(trend=True)
    context = {'prods': product_list,
               }
    return render(request, 'customer/homepage.html', context)


@auth_customer
def productdetails_page(request, pid):
    msg = ''
    products_details = Product.objects.get(id=pid)
    if request.method == 'POST':
        product_size = request.POST['p_size']
        product_exist = Cart.objects.filter(
            product=pid, customer=request.session['customer']).exists()
        if not product_exist:
            cart = Cart(
                customer_id=request.session['customer'], product_id=products_details.id)
            cart.product_size = product_size
            cart.save()
            msg = 'Item added to cart'
        else:
            msg = 'Item already in cart'
    context = {'details': products_details,
               'msg': msg
               }
    return render(request, 'customer/viewproduct.html', context)


@auth_customer
def cart_page(request):
    product_cart = Cart.objects.filter(customer=request.session['customer']).annotate(
        total=F('product__price')*F('product_quantity')).order_by('id')
    return render(request, 'customer/cart.html', {'cart_list': product_cart})


@auth_customer
def profile_page(request):
    msg = ''
    cust_list = Customer.objects.get(id=request.session['customer'])
    if request.method == 'POST':
        customer = Customer.objects.get(id=request.session['customer'])

        customer_name = request.POST['c_name']
        email_address = request.POST['c_email']
        address = request.POST['c_address']
        phone_number = request.POST['c_number']

        customer.customer_name = customer_name
        customer.email_address = email_address
        customer.address = address
        customer.phone_number = phone_number
        customer.save()
        msg = 'Profile updated successfully'
    context = {
        'custs': cust_list,
        'msg': msg
    }
    return render(request, 'customer/profile.html', context)


@auth_customer
def allview_page(request):
    product_list = Product.objects.all().order_by('product_name')
    return render(request, 'customer/allview.html', {'prods': product_list})


@auth_customer
def category_page(request, data=None):
    if data == None:
        products = Product.objects.all().order_by('product_name')
    elif data == 'Shirt' or data == 'T-shirt' or data == 'Pant' or data == 'Accessories' or data == 'Shoes' or data == 'Casuals' or data == 'Innerwears':
        products = Product.objects.filter(product_cat=data)
    return render(request, 'customer/category.html', {'prods': products})


def remove_item(request, pid):
    cart_item = Cart.objects.get(
        product=pid, customer=request.session['customer'])
    cart_item.delete()
    return redirect('customer:cartpage')


def logout(request):
    del request.session['customer']
    request.session.flush()
    return redirect('common:custlogin')


@auth_customer
def wishlist_page(request):
    product_wishlist = Wishlist.objects.filter(
        customer=request.session['customer'])
    context = {'wish_list': product_wishlist}
    return render(request, 'customer/wishlist.html', context)


# def add_to_wishlist(request, pid):
#     product_exist = Wishlist.objects.filter(product=pid, customer=request.session['customer']).exists()
#     if not product_exist:
#         wishlist = Wishlist(customer_id=request.session['customer'], product_id=pid)
#         wishlist.save()
#         return redirect('customer:wishlist')

#     else:
#         return redirect('customer:wishlist')


def removewish_item(request, pid):
    wishlist_item = Wishlist.objects.get(
        product=pid, customer=request.session['customer'])
    wishlist = request.session.get('wishlist', [])
    if pid in wishlist:
        wishlist.remove(pid)
        request.session['wishlist'] = wishlist
    wishlist_item.delete()
    return redirect('customer:wishlist')


@auth_customer
def checkout_page(request):
    product_cart = Cart.objects.filter(customer=request.session['customer'])
    total_price = 50
    for item in product_cart:
        total_price = total_price + item.product.price * item.product_quantity
    context = {
        'cart_list': product_cart,
        'total_price': total_price
    }
    return render(request, 'customer/checkout.html', context)


def search_page(request):
    if request.method == 'POST':
        search_word = request.POST['searchdata']
        searchproducts = Product.objects.filter(Q(product_name__icontains=search_word) |
                                                Q(product_description__icontains=search_word) |
                                                Q(price__icontains=search_word) |
                                                Q(product_cat__icontains=search_word)).order_by('product_name')
        return render(request, 'customer/searchprod.html', {'searchprod': searchproducts})
    else:
        return redirect('customer/search')


@auth_customer
def pass_page(request):
    msg = ''
    cust_data = Customer.objects.get(id=request.session['customer'])
    if request.method == 'POST':
        customer = Customer.objects.get(id=request.session['customer'])

        current_pass = request.POST['current_pass']
        new_pass = request.POST['new_pass']
        confirm_pass = request.POST['confirm_pass']

        if customer.cust_password == current_pass:

            if new_pass == confirm_pass:
                customer.cust_password = new_pass
                customer.save()
                msg = 'Password changed succesfully'

            else:
                msg = 'Password does not match'

        else:
            msg = 'Incorrect Password'
    context = {'msg': msg,
               'data': cust_data,
               }
    return render(request, 'customer/pass.html', context)


def quantity(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if (Cart.objects.filter(customer_id=request.session['customer'], product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(
                customer_id=request.session['customer'], product_id=prod_id)
            cart.product_quantity = prod_qty
            cart.save()
            return JsonResponse({'success': True})


def add_to_wishlist(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        wishlist = request.session.get('wishlist', [])
        product_exist = Wishlist.objects.filter(
            product=prod_id, customer=request.session['customer']).exists()
        if prod_id not in wishlist:
            wishlist.append(prod_id)
            request.session['wishlist'] = wishlist
            if not product_exist:
                wishlist = Wishlist(
                    customer_id=request.session['customer'], product_id=prod_id)
                wishlist.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Product already exists in wishlist.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Product already exists in wishlist.'})
    return redirect('customer:wishlist')


@auth_customer
def order_page(request):
    orders = Order.objects.filter(customer=request.session['customer'])
    context = {
        'orders': orders
    }
    return render(request, 'customer/order.html', context)


@auth_customer
def view_order(request, t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(
        customer=request.session['customer']).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'orderitems': orderitems
    }
    return render(request, 'customer/vieworder.html', context)


def total_price(request):
    qty = request.POST['qty']
    pid = request.POST['pid']
    product = Product.objects.filter(id=pid).values('price')
    total = int(qty)*product[0]['price']
    return JsonResponse({'total': total})


def placeorder(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.customer = Customer.objects.get(
            id=request.session['customer'])
        neworder.first_name = request.POST.get('first_name')
        neworder.last_name = request.POST.get('last_name')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.ph_number = request.POST.get('ph_number')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')

        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        cart = Cart.objects.filter(customer=request.session['customer'])
        cart_total_price = 50
        for item in cart:
            cart_total_price = cart_total_price+item.product.price*item.product_quantity
        neworder.total_price = cart_total_price
        trackno = 'mensview'+str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'mensview'+str(random.randint(1111111, 9999999))
        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(
            customer=request.session['customer'])
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                seller=item.product.seller,
                price=item.product.price,
                quantity=item.product_quantity,
                prod_size=item.product_size
            )

            orderproduct = item.product
            orderproduct.current_stock = orderproduct.current_stock - item.product_quantity
            orderproduct.save()
        cart_item = Cart.objects.filter(customer=request.session['customer'])
        cart_item.delete()
        paymode = request.POST.get('payment_mod')
        if (paymode == 'paid by razorpay'):
            return JsonResponse({'status': 'your order has been placed successfully'})

    return redirect('customer:homepage')


def payonline(request):
    cart = Cart.objects.filter(customer=request.session['customer'])
    total_price = 50
    for item in cart:
        total_price = total_price+item.product.price*item.product_quantity
    return JsonResponse({'total_price': total_price})


def myorder_page(request):
    return HttpResponse('my order')
