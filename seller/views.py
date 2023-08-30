from django.shortcuts import render,redirect
from common.models import Seller,Customer
from customer.models import Order,OrderItem
from . models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def master_page(request):   
    return render(request,'seller/master.html')
def home_page(request):
    seller_data = Seller.objects.get(id=request.session['seller'])
    seller_products = Product.objects.filter(seller = request.session['seller'])
    products_count = seller_products.count()
    order =OrderItem.objects.filter(seller=request.session['seller']).order_by('-id')[:7]
    orderitem =OrderItem.objects.filter(seller=request.session['seller'])
    order_count = orderitem.count()
    delivered = OrderItem.objects.filter(seller=request.session['seller'],item_status='delivered')
    delivered_count = delivered.count()
    percentage = (delivered_count / order_count) * 100 if delivered_count > 0 else 0
    context = {
        'data' : seller_data,
        'products_count': products_count,
        'order_count':order_count,
        'order':order,
        'delivered_count':delivered_count,
        'percentage':percentage
    }
    return render(request,'seller/homepage.html',context)
def orders_page(request):
    seller_data = Seller.objects.get(id=request.session['seller'])
    orders = OrderItem.objects.filter(seller=request.session['seller'])
    context = {'orders': orders,'data': seller_data}
    return render(request,'seller/orders.html',context)
def product_page(request):
    seller_products = Product.objects.filter(seller = request.session['seller'])
    seller_data = Seller.objects.get(id=request.session['seller'])
    context ={'products':seller_products,
                'data': seller_data,
                }
    return render(request,'seller/products.html',context)
def addprod_page(request):
    msg = ''
    seller_data = Seller.objects.get(id=request.session['seller'])
    if request.method == 'POST':
        product_name = request.POST['p_name']
        product_description = request.POST['p_description']
        product_cat = request.POST['p_cat']
        product_number = request.POST['p_number']
        current_stock = request.POST['current_stock']
        product_image = request.FILES['p_image']
        price = request.POST['price']
        if Product.objects.filter(product_name=product_name).exists():
            messages.error(request, 'A product with this product name already exists.')
            return redirect('seller:addprod')



        new_product = Product(product_name=product_name, product_description=product_description,product_cat = product_cat, product_number=product_number,
                              current_stock=current_stock, product_image=product_image, price=price, seller_id=request.session['seller'])
        new_product.save()
        msg = "product added successfully"
    return render(request,'seller/addprod.html',{'msg':msg,'data': seller_data})
def updateprod_page(request):
    seller_data = Seller.objects.get(id=request.session['seller'])
    product_data = Product.objects.filter(seller=request.session['seller'])

    if request.method == 'POST':
        new_stock = request.POST['new_stock']
        product_id = request.POST['productid']
        new_price = request.POST['new_price']

        product = Product.objects.get(id=product_id)
        product.current_stock = product.current_stock + int(new_stock)
        product.price = new_price

        product.save()
    context = {'prod_data': product_data,
                    'data': seller_data,
                    }

    return render(request,'seller/updateprod.html',context)
def sprofile_page(request):
    msg=''
    seller = Seller.objects.get(id=request.session['seller'])
    if request.method=='POST':
        # seller = Seller.objects.get(id = request.session['seller'])

        seller_name = request.POST['s_name']
        seller_email = request.POST['s_email']
        seller_address = request.POST['s_address']
        seller_number = request.POST['s_phone']
        company_name = request.POST['comp_name']
        accholder = request.POST['accholder_name']
        branch = request.POST['s_branch']
        ifsc = request.POST['s_ifsc']
        seller_image = request.FILES['s_image']
        acc_number = request.POST['accnum']

        seller.seller_name = seller_name
        seller.seller_email = seller_email
        seller.address = seller_address
        seller.phone_number = seller_number
        seller.comp_name = company_name
        seller.accholder_name = accholder
        seller.ifsc = ifsc
        seller.branch = branch
        seller.sell_pic = seller_image
        seller.acc_number=acc_number
        seller.save()
        msg = 'Profile updated successfully'
    context = {
        'data': seller,
        'msg':msg
    }
    return render(request,'seller/sprofile.html',context)
def pdetails_page(request,pid):
    products_details = Product.objects.get(id = pid)
    products_details.trend=True
    products_details.save()
    context ={'details':products_details,
                }
    return render(request,'seller/pdetails.html',context)
def logout(request):
    del request.session['seller'] 
    request.session.flush()
    return redirect('common:selllogin')
def get_stock(request):
    id = request.POST['id']
    product =Product.objects.get(id=id)
    product_name = product.product_name
    current_stock = product.current_stock
    price = product.price
    product_id = product.id
    return JsonResponse({'p_name':product_name,'stock':current_stock,'p_id':product_id,'price':price})
def delete_prod(request,sid):
    prod_list = Product.objects.get(id = sid)
    prod_list.delete()
    return redirect('seller:product')
def sellpass_page(request):
    msg =''
    seller_data = Seller.objects.get(id=request.session['seller'])
    if request.method == 'POST':
        seller = Seller.objects.get(id = request.session['seller'])

        current_pass = request.POST['current_pass'] 
        new_pass = request.POST['new_pass'] 
        confirm_pass = request.POST['confirm_pass']

        if seller.seller_pass == current_pass:

            if new_pass == confirm_pass:
                 seller.seller_pass = new_pass
                 seller.save()
                 msg = 'Password changed succesfully'

            else:
                msg = 'Password does not match'

        else:
            msg = 'Incorrect Password'
    context =  {'msg':msg,
                'data': seller_data,
                }
    return render(request, 'seller/sellpass.html',context)

def sellerorderdetails(request, order_id):
    seller_data = Seller.objects.get(id=request.session['seller'])
    order =OrderItem.objects.filter(order=order_id, seller=request.session['seller']).first()
    context = {'order': order,'data': seller_data}
    return render(request, 'seller/orderdetails.html', context)
def mark_as_delivered(request, s_id,o_id):
    order = OrderItem.objects.filter(seller=s_id,order=o_id)
    for order in order:
        order.item_status = 'delivered'
        order.save()
    return redirect('seller:orders')
def product_exist(request):
    product = request.POST['product']

    status = Product.objects.filter(product_name = product).exists()

    return JsonResponse({'status':status})
