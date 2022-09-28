from itertools import product
from django.shortcuts import render, redirect
from .models import DeliveryOption, Product, ProductImage, Order, OrderedProduct, Address, Payment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import random
import string
from .forms import CheckoutForm

import json
from django.http import HttpResponseRedirect, JsonResponse

from django.conf import settings


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

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, K=20))

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
    try:
        order = Order.objects.get(user = request.user, ordered= False)
        delivery_option = DeliveryOption.objects.all()
        form = CheckoutForm()
        
        context = {
            'deliveryOption' : delivery_option,
            'form' :form
        }
        if request.method == "POST":
            form = CheckoutForm(request.POST or None)
            if form.is_valid():       
                address1  = request.POST['address']
                address2 = request.POST['address2']
                country = form.cleaned_data.get('shipping_country')
                zip = request.POST['zip']
                deliveryOptionName = request.POST['deliveryOption']
                
                if form_validation([address1, address2, country, zip, deliveryOptionName]):
                    deliveryOption = DeliveryOption.objects.get(delivery_name=deliveryOptionName)
                
                    address, created =Address.objects.get_or_create(
                        user=request.user,
                        street_address=address1,
                        apartment_address=address2,
                        country=country,
                        zip=zip
                    )
                    address.save()
                    order.delivery_option = deliveryOption
                    order.shipping_address = address
                    order.save()
                
                
                return redirect('checkout-page')
            else:
                return redirect('checkout-page') 
        
        return render(request, 'checkout.html', context) 
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order to proceed to checkout")
        return redirect ('/')    
    
def paymentPage(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        context ={
                'order': order,
                'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID
            }
        print(settings.PAYPAL_CLIENT_ID)
        return render(request, 'paypal_payment.html', context)
        '''if order.delivery_option and order.shipping_address:
            context ={
                'order': order
            }
            
            return render(request, 'paypal_payment.html', context)
        else:
            messages.info(request, "You haven't checked out")
            return redirect('/')'''
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order to proceed to checkout")
        return redirect('/')

def payment_complete(request):  
    order = Order.objects.get(user= request.user, ordered=False)
    body = json.loads(request.body)
    orderId = body["order_id"]
    paymentId = body["payment_id"]
    status = body["status"]
    amount = body["amount"]
    user = request.user
    
    print(orderId)
    print(paymentId)
    print(status)
    print(amount)
    
    if status == "COMPLETED":
        payment_date = timezone.now()
        payment = Payment.objects.create(
            paypal_id = paymentId,
            user= user,
            amount= amount,        
        )
        
        order_products = order.products.all()
        order_products.update(ordered=True)
        for orderedProduct in order_products:
            orderedProduct.save()
            
        order.payment=payment
        order.ordered=True
        order.ref_number = orderId
        order.save()
        
        #messages.success(request, "Your payment was successful and your order has been received!")
    
    
    return JsonResponse("Payment completed", safe=False)
