from django.db import models
from django.forms import ModelForm
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=100);
    brand=models.CharField(max_length=100);
    description=models.TextField();
    category=models.CharField(max_length=100);
    price=models.IntegerField();
    quantity=models.IntegerField();
    colors=ArrayField(ArrayField(models.CharField(max_length=100)));
    # models.Choices
    image=models.ImageField(upload_to='pics');
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
