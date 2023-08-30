from django.urls import path
from . import views

app_name = 'mensviewadmin'
urlpatterns = [
    path('master',views.master_page,name='master'),
    path('adminlogin',views.adminlogin_page,name='adminlogin'),
    path('adminhome',views.adminhome_page,name='adminhome'),
    path('approve',views.approve_page,name='approve'),
    path('viewsellers',views.viewsellers_page,name='viewsellers'),
    path('viewcust',views.viewcust_page,name='viewcust'),
    path('viewprod',views.viewprod_page,name='viewprod'),
    path('approve/<int:sid>',views.approve,name='approve'),
    path('deletesell/<int:sid>',views.delete_seller,name='deletesell'),
    path('deletecust/<int:sid>',views.delete_cust,name='deletecust'),
    path('deleteprod/<int:sid>',views.delete_prod,name='deleteprod'),
    path('trend/<int:pid>',views.trend,name='trend'),
    path('untrend/<int:pid>',views.un_trend,name='untrend'),
]
