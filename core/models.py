from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase




User = get_user_model()

SALE_CHOICES = (
    ('S', 'Sport'),
    ('lX', 'Luxury'),
)
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)
WEAR_CHOICES = (
    ('Dr', 'Dress'),
    ('Sh', 'Shoe'),
)
ACCESSORY_CHOICES = (
    ('w', 'Watch'),
    ('B', 'Bag'),
    ('GL', 'Glass'),
)

PRODUCT_COLOUR = (
    ('Pink', 'Pink'),
    ('BLue', 'Blue'),
    ('Gold', 'Gold'),
    ('Black', 'Black'),
    ('Red', 'Red'),
    ('Orange', 'Orange'),
)

PRODUCT_SIZE = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
)


DELIVERY_CHOICES = [
    ("IS", "In Store"),
    ("HD", "Home Delivery"),
    ("DD", "Digital Delivery"),
]

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=2)
    sale_type = models.CharField(choices=SALE_CHOICES, max_length=2)
    accessory_type = models.CharField(choices=ACCESSORY_CHOICES, max_length=2, blank=True)
    colour = MultiSelectField(choices=PRODUCT_COLOUR, max_length=31)
    size = MultiSelectField(choices=PRODUCT_SIZE, max_length=10)
    is_featured = models.BooleanField(default=False)
    tags = TaggableManager(through=UUIDTaggedItem)

    
      
    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='image', on_delete=models.CASCADE)
    image = models.ImageField()
        
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="productReview")
    content = models.TextField()
    
    def __str__(self):
        return self.user.username

class OrderedProduct(models.Model):
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=4,)
    colour = models.CharField(max_length=10, default='Black')
    ordered = models.BooleanField(default=False)
 
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_total_item_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderedProduct)
    ref_number = models.CharField(max_length=20, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    delivery_option = models.ForeignKey('DeliveryOption', on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_item_price()
            
        if self.delivery_option:
            total += self.delivery_option.delivery_price
                      
        return total


class Address(models.Model):
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    
    def __str__(self):
        return self.street_address
    
    class Meta:
        verbose_name_plural = 'Addresses'
        

class DeliveryOption(models.Model):
    delivery_name = models.CharField(max_length=255,)
    delivery_price = models.FloatField()
    delivery_method = models.CharField(choices=DELIVERY_CHOICES, max_length=255,)
    delivery_timeframe = models.CharField(max_length=255)
    
    def __str__(self):
        return self.delivery_name
       
    
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
    
