from itertools import product
from django.shortcuts import render, redirect
from .models import Product, ProductImage, Order, OrderedProduct
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    
    return render(request, 'index.html')

def shopPage(request):
    product = Product.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(product, 6)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    context = {
        'product': product,
        'page': page
    }
    
    return render(request, 'shop.html', context)

def menPage(request):
    product = Product.objects.filter(gender='M')
    page = request.GET.get('page')
    paginator = Paginator(product, 6)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    context = {
        'product': product,
        'page': page
    }
    
    return render(request, 'shop.html', context)
    
   
def womenPage(request):
    product = Product.objects.filter(gender='F')
    page = request.GET.get('page')
    paginator = Paginator(product, 6)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    context = {
        'product': product,
        'page': page
    }
    
    return render(request, 'shop.html', context)

def cartPage(request, pk):
    product = Product.objects.get(id = pk)
    
    context={
        'product':product
    }

    return render(request, 'shop-single.html', context)


def form_validation(values):
    valid = True
    for field in values:
        if field == "":
            valid = False
    return valid

def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    
    if request.method == "POST":
        size = request.POST['product-size']
        colour = request.POST['colour']
        quantity = request.POST['product-quanity']
        
        if form_validation([size, colour,quantity]):
        
            ordered_product, created = OrderedProduct.objects.get_or_create(
                product = product,
                user=request.user,
                ordered=False,
                colour = colour,
                size = size
            )
            
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                if order.products.filter(product__id=product.id, colour=colour, size=size).exists():
                    ordered_product.quantity += int(quantity)
                    ordered_product.save()
                    messages.info(request, "this item was updated to your cart")
                    return redirect('cart-page', pk = pk)
                    
                else: 
                    ordered_product.quantity = quantity
                    ordered_product.save()
                    order.products.add(ordered_product)
                    messages.info(request, "this item was added to your cart")
                    return redirect('cart-page', pk = pk)
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(user=request.user, ordered_date=ordered_date)
                order.products.add(ordered_product)
                messages.info(request, "this item was added to your cart")
                return redirect('cart-page', pk = pk)
        else:
            messages.info(request, "Please select all fields")
            return redirect('cart-page', pk = pk)
        

def remove_from_cart(request, pk, colour, size):
    product = Product.objects.get(id=pk)
      
    ordered_product= OrderedProduct.objects.get(product = product, user=request.user, ordered=False, colour = colour, size = size)
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=product.id, colour=colour, size=size).exists():     
            order.products.remove(ordered_product)
            ordered_product.delete()
            messages.info(request, "this item was removed from your cart")
            return redirect('order-page')
            
        else: 
            messages.info(request, "Product wasn't in your cart")
            return redirect('order-page')
    else:
        messages.info(request, "Your don't have an order")
        return redirect('/')
    
def add_singleQuantity_to_product(request, pk, colour, size):
    product = Product.objects.get(id=pk)
      
    ordered_product= OrderedProduct.objects.get(product = product, user=request.user, ordered=False, colour = colour, size = size)
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=product.id, colour=colour, size=size).exists():     
            if ordered_product.quantity < 10:
                ordered_product.quantity += 1
                ordered_product.save()
                return redirect('order-page')
            else:
                messages.info(request, "Maximum quantity per product reached")
                return redirect('order-page')
            
        else: 
            messages.info(request, "Product wasn't in your cart")
            return redirect('order-page')
    else:
        messages.info(request, "Your don't have an order")
        return redirect('/')
    
def remove_singleQuantity_from_product(request, pk, colour, size):
    product = Product.objects.get(id=pk)
      
    ordered_product= OrderedProduct.objects.get(product = product, user=request.user, ordered=False, colour = colour, size = size)
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=product.id, colour=colour, size=size).exists():     
            if ordered_product.quantity > 1:
                ordered_product.quantity -= 1
                ordered_product.save()
                return redirect('order-page')
            else:
                order.products.remove(ordered_product)
                ordered_product.delete()
                messages.info(request, "this item was removed from your cart")
                return redirect('order-page')
            
        else: 
            messages.info(request, "Product wasn't in your cart")
            return redirect('order-page')
    else:
        messages.info(request, "Your don't have an order")
        return redirect('/')
      
        
def orderSummaryPage(request):
    try:
        order = Order.objects.get(user = request.user, ordered = False)
        print(order.products)
        context ={
            'order':order
        }
        
        return render(request, 'cart_page.html', context)
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order")
        return redirect("/")

    
def checkoutPage(request):
    
    return render(request, 'checkout.html')        