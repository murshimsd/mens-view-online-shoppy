from django.urls import path
from . import views

app_name = 'seller'
urlpatterns = [
    path('master',views.master_page,name='master'),
    path('home',views.home_page,name='homepage'),
    path('orders',views.orders_page,name='orders'), 
    path('product',views.product_page,name='product'),    
    path('addprod',views.addprod_page,name='addprod'), 
    path('sellpass',views.sellpass_page,name='sellpass'), 
    path('updateprod',views.updateprod_page,name='updateprod'), 
    path('sprofile',views.sprofile_page,name='sprofile'), 
    path('pdetails/<int:pid>',views.pdetails_page,name='pdetails'),
    path('logout',views.logout,name='logout'),
    path('getstock', views.get_stock, name='getstock'),
    path('deleteprod/<int:sid>',views.delete_prod,name='deleteprod'),
    path('orderdetails/<int:order_id>',views.sellerorderdetails,name='orderdetails'),
    path('delivered/<int:s_id>/<int:o_id>',views.mark_as_delivered,name='delivered'),
    path('product_exist',views.product_exist,name='product_exist'),
]