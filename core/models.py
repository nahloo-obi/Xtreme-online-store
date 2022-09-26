from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django_countries.fields import CountryField


User = get_user_model()

CATEGORY_CHOICES = (
    ('s', 'Shirt '),
    ('sw', 'Sport wear'),
    ('ow', 'Outwear')
)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    description = models.TextField()
      
    def __str__(self):
        return self.title
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='image', on_delete=models.CASCADE)
    image = models.ImageField()
        

class OrderedProduct(models.Model):
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
 
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_total_item_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderedProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        
        if self.coupon:
            total -= self.coupon.amount          
        return total


class Address(models.Model):
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Addresses'
    
    
class Payment(models.Model):
    paypal_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username    
    
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    
    def __str__(self) -> str:
        return f"{self.pk}"
    
