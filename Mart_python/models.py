from django.db import models
from statistics import mode
from django.forms import ModelForm
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Registration(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    mobileNo = models.BigIntegerField()
    category = models.CharField(max_length=100)

class Product(models.Model):
    name=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    description=models.TextField()
    category=models.CharField(max_length=100)
    price=models.IntegerField()
    quantity=models.IntegerField()
    colors=ArrayField(ArrayField(models.CharField(max_length=100)))
    # models.Choices
    image=models.ImageField(upload_to='pics')
    customer = models.ForeignKey(Registration, on_delete=models.CASCADE)

class Cart(models.Model):
    productId=models.IntegerField()
    customerId=models.IntegerField()
    productName=models.CharField(max_length=100)
    quantity=models.IntegerField()
    image=models.CharField(max_length=255)
    price=models.IntegerField()

class Order(models.Model):
    customerId=models.IntegerField()
    address=models.CharField(max_length=500)
    method = models.CharField(max_length=500)
    date = models.CharField(max_length=200)

class DeatiledOrder(models.Model):
    orderId = models.IntegerField()
    customerId = models.IntegerField()
    productId=models.IntegerField()
    productName=models.CharField(max_length=100)
    quantity=models.IntegerField()
    price=models.IntegerField()
    
# class ProductForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = "__all__"