from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField(default='uploads/products/funsush.jpg',upload_to='uploads/category/')
    def __str__(self):
        return self.name




class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=20)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.first_name}{self.last_name}'

class Product(models.Model):
    name=models.CharField(max_length=150)
    price=models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description=models.CharField(max_length=250,default='',blank=True,null=True)
    image=models.ImageField(upload_to='uploads/product/')
    stocks=models.IntegerField(default=0)
    def __str__(self):
        return self.name
    

class Order(models.Model):
    PEND = 'Pending'
    ONDELIVERY = 'On Delivery'
    DELIVERED = 'Delivered'
    STATUS_CHOICES = (
        (PEND, 'Pending'),
        (ONDELIVERY, 'On Delivery'),
        (DELIVERED, 'Delivered'),
    )
    COD='Pay On Delivery'
    ONLPAY='Khalti Payment'
    PAYMENT_CHOICES=(
        (COD, 'Pay on delivery'),
        (ONLPAY, 'Khalti Payment'),

    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.CharField(max_length=100,default='',blank=False)
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=100,default='',blank=True)
    phone=models.CharField(max_length=20,default='',blank=True)
    date=models.DateField(default=datetime.datetime.today)
    payment_type=models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=COD)
    order_status=models.CharField(max_length=20, choices=STATUS_CHOICES, default=PEND)

    def __str__(self):
        return self.customer

