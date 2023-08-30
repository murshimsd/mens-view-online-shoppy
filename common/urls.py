from django.urls import path
from . import views

app_name = 'common'
urlpatterns = [
    path('',views.commonhome_page,name='common'),
    path('custreg',views.custreg_page,name='custreg'),
    path('sellreg',views.sellreg_page,name='sellreg'),
    path('selllogin',views.selllogin_page,name='selllogin'),
    path('custlogin',views.custlogin_page,name='custlogin'),
    path('allview',views.allview_page,name='allview'), 
    path('email_exist',views.email_exist,name='email_exist'),
    path('sellermail_exist',views.sellermail_exist,name='sellermail_exist'),
    path('compname_exist',views.compname_exist,name='compname_exist'),
    path('accno_exist',views.accno_exist,name='accno_exist'),
    # path('details',views.productdetails_page,name='detailspage'),    
]