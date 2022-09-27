from django.contrib import admin
from .models import Product, Order, OrderedProduct, ProductImage

class ProductImage(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImage]

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderedProduct)




