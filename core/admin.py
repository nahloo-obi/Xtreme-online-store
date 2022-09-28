from django.contrib import admin
from .models import Product, Order, OrderedProduct, ProductImage, DeliveryOption, Address, Payment

class ProductImage(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImage]

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderedProduct)
admin.site.register(DeliveryOption)
admin.site.register(Address)
admin.site.register(Payment)




