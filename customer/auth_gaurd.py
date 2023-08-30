from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def auth_customer(func):
    def wrapper(request,*args,**kwargs):
        if 'customer' in request.session: # customer is key in session 
           
            return func(request,*args,**kwargs) #call function
        else:
             return redirect('common:custlogin')
    return wrapper