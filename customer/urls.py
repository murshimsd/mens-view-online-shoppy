from django.urls import path
from . import views

app_name = 'customer'
urlpatterns = [
    path('master',views.master_page,name='master'),
    path('home',views.home_page,name='homepage'), 
    path('details/<int:pid>',views.productdetails_page,name='detailspage'),    
    path('cart',views.cart_page,name='cartpage'),
    path('pass',views.pass_page,name='passpage'), 
    path('wishlist',views.wishlist_page,name='wishlist'), 
    path('profile',views.profile_page,name='profile'), 
    path('allview',views.allview_page,name='allview'),
    path('category',views.category_page,name='category'), 
    path('category/<str:data>',views.category_page,name='categorywise'), 
    path('remove_cart/<int:pid>',views.remove_item,name='remove_cart'),
    path('remove_wish/<int:pid>',views.removewish_item,name='remove_wish'),
    path('logout',views.logout,name='logout'),
    # path('addwishlist/<int:pid>',views.add_to_wishlist, name="addwishlist"),
    path('checkout',views.checkout_page,name='checkout'),
    path('search',views.search_page,name='search'),
    path('quantity',views.quantity,name='quantity'),
    path('order',views.order_page,name='order'),
    path('vieworder/<str:t_no>',views.view_order,name='vieworder'),
    path('totalprice',views.total_price,name='total_price'),
    path('payonline',views.payonline,name='payonline'),
    path('placeorder',views.placeorder,name='placeorder'),
    path('myorder',views.myorder_page,name='myorder'),
    path('addtowishlist',views.add_to_wishlist, name="addtowishlist"),
]