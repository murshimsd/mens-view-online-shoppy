from django.db import models
from seller.models import Product
from common.models import Customer,Seller
# Create your models here.
class Cart(models.Model):
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    customer =  models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=50,default='')
    product_quantity = models.IntegerField(default='1')

class Wishlist(models.Model):
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    customer =  models.ForeignKey(Customer, on_delete=models.CASCADE)

class Order(models.Model):
    customer =  models.ForeignKey(Customer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    ph_number = models.BigIntegerField()
    total_price = models.FloatField()
    payment_mode = models.CharField(max_length=150,null=False)
    payment_id = models.CharField(max_length=250,null=True)
    status = models.CharField(max_length=250,default='pending')
    tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    prod_size = models.CharField(max_length=10,default='')
    item_status = models.CharField(max_length=250,default='pending')










