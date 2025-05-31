from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    seller = models.ForeignKey(User , on_delete=models.CASCADE , default=1)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    file = models.FileField(upload_to='products/')
    total_sales_amount = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_email = models.EmailField()
    quantity = models.IntegerField(default=1)
    amount = models.IntegerField(default=0)
    has_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    
    