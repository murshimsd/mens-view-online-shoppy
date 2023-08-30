from django.db import models

# Create your models here.    
class Customer(models.Model):
    customer_name = models.CharField(max_length=20)
    email_address = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    phone_number = models.BigIntegerField()
    gender = models.CharField(max_length=50)
    cust_password = models.CharField(max_length=10)

class Seller(models.Model):
    seller_name = models.CharField(max_length=20)
    seller_email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    gender = models.CharField(max_length=50)
    comp_name = models.CharField(max_length=100)
    accholder_name = models.CharField(max_length=30)
    ifsc = models.CharField(max_length=30)
    branch = models.CharField(max_length=20)
    seller_pass = models.CharField(max_length=20)
    acc_number = models.BigIntegerField()
    sell_pic = models.ImageField(upload_to='sellerimg/')
    approved = models.BooleanField(default=False)
