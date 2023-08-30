from django.shortcuts import render,redirect
from common.models import Customer,Seller
from customer.models import OrderItem
from seller.models import Product
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def master_page(request):   
    return render(request,'mensviewadmin/master.html')
def adminlogin_page(request):
    return render(request,'mensviewadmin/adminlogin.html')
def adminhome_page(request):
    last_five_cust = Customer.objects.order_by('-id')[:6]
    customers = Customer.objects.all()
    cust_count = customers.count()
    product_list = Product.objects.all()
    prod_count = product_list.count()
    sellers = Seller.objects.filter(approved=True).order_by('-id')[:6]
    sellers_count = sellers.count()
    order =OrderItem.objects.all()
    order_count = order.count()
    delivered = OrderItem.objects.filter(item_status='delivered')
    delivered_count = delivered.count()
    percentage = (delivered_count / order_count) * 100 if delivered_count > 0 else 0
    context = {
        'seller_list':sellers,
        'prods': product_list,
        'cust_count':cust_count,
        'prod_count':prod_count,
        'sellers_count':sellers_count,
        'percentage':percentage,
        'last_five_cust':last_five_cust,
    }
    return render(request,'mensviewadmin/adminhome.html',context)
def approve_page(request):
    sellers = Seller.objects.filter(approved = False).order_by('id')
    return render(request,'mensviewadmin/approve.html',{'seller_app':sellers})
def viewsellers_page(request):
    sellers = Seller.objects.filter(approved=True).order_by('id')
    return render(request,'mensviewadmin/viewsellers.html',{'seller_list':sellers})
def viewcust_page(request):
    customers = Customer.objects.all().order_by('id')
    context = {
        'customer_list':customers
    }
    return render(request,'mensviewadmin/viewcust.html',context)
def viewprod_page(request):
    product_list = Product.objects.all().order_by('trend')
    seller_data = Seller.objects.all()
    context =  {'prods': product_list,
                'data': seller_data,
                }
    return render(request,'mensviewadmin/viewprod.html',context)
def approve(request,sid):
    seller=Seller.objects.get(id=sid)
    message = ' Welcome to MENSVIEW OFFICIAL SHOPPING WEBSITE you can now login to your account, Thanks you'
    send_mail(
        'Login Approved',
        message,
        settings.EMAIL_HOST_USER,
        [seller.seller_email,], 
    )
    seller.approved=True
    seller.save()
    return redirect('mensviewadmin:viewsellers')
def delete_seller(request,sid):
    seller_list = Seller.objects.get(id = sid)
    seller_list.delete()
    return redirect('mensviewadmin:viewsellers')
def delete_cust(request,sid):
    cust_list = Customer.objects.get(id = sid)
    cust_list.delete()
    return redirect('mensviewadmin:viewcust')
def delete_prod(request,sid):
    prod_list = Product.objects.get(id = sid)
    prod_list.delete()
    return redirect('mensviewadmin:viewprod')
def trend(request,pid):
    prod=Product.objects.get(id=pid)
    prod.trend=True
    prod.save()
    return redirect('mensviewadmin:viewprod')
def un_trend(request,pid):
    prod=Product.objects.get(id=pid)
    prod.trend=False
    prod.save()
    return redirect('mensviewadmin:viewprod')
