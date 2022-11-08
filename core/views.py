from itertools import product
from django.shortcuts import render, redirect, reverse
from .models import DeliveryOption, Product, ProductImage, Order, OrderedProduct, Address, Payment, ProductReview
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import random
import string
from .forms import CheckoutForm, ReviewForm
from django.views.generic import View, ListView, DetailView

from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User, auth

from django.conf import settings
import random
from hitcount.views import HitCountDetailView
from .filters import Productfilters



def index(request):
    featured_products = list(Product.objects.filter(is_featured = True))
    if len(featured_products) >3:
        product = random.sample(featured_products, 3)
    else:
        product = Product.objects.filter(is_featured = True)
   
    context = {
        "product" : product
    }
    
    return render(request, 'index.html', context)

""" 
def shopPage(request):
    products = list(Product.objects.all())
    count = len(products)
    product = random.sample(products, count)
    
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
"""

def shopPage(request):
    products = Product.objects.all().order_by('id')
    product = Productfilters(request.GET, queryset=products)
    
    page = request.GET.get('page')
    paginator = Paginator(product.qs, 6)
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context = {
        'product': response,
        'page': page,
        'product_filter' : product
    }
    
    return render(request, 'shop.html', context)
    
   
def genderFilterPage(request, gender):
    if gender =="Male":
        product = Product.objects.filter(gender="M")
    else:
        product = Product.objects.filter(gender="F")
    products = Productfilters(request.GET, queryset=product)
    page = request.GET.get('page')
    paginator = Paginator(products.qs, 6)
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context = {
        'product': response,
        'page': page,
        'product_filter' : products
    }
    
    return render(request, 'shop.html', context)


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
                    return redirect('product-page', pk = pk)
                    
                else: 
                    ordered_product.quantity = quantity
                    ordered_product.save()
                    order.products.add(ordered_product)
                    messages.info(request, "this item was added to your cart")
                    return redirect('product-page', pk = pk)
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(user=request.user, ordered_date=ordered_date)
                order.products.add(ordered_product)
                messages.info(request, "this item was added to your cart")
                return redirect('product-page', pk = pk)
        else:
            messages.info(request, "Please select all fields")
            return redirect('product-page', pk = pk)
        

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
      
@login_required(login_url='signin')      
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

@login_required(login_url='signin')    
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
   
@login_required(login_url='signin')  
def paymentPage(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        if order.delivery_option and order.shipping_address:
            context ={
                'order': order,
                'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID
            }
            
            return render(request, 'paypal_payment.html', context)
        else:
            messages.info(request, "You haven't checked out")
            return redirect('/')
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order to proceed to payment")
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


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop-single.html"
    #count_hit = True
    
    form = ReviewForm()
    
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            product = self.get_object()
            form.instance.user = request.user
            form.instance.product = product
            form.save()
            
            return redirect(reverse("product-page", kwargs={
                'pk':product.id
            }))
            
    def get_context_data(self, **kwargs):
        similar_post = self.object.tags.similar_objects()[:3]
        product_review = ProductReview.objects.all().filter(product=self.object.id)
        product_review_count = ProductReview.objects.all().filter(product=self.object.id).count()
        product = self.get_object()
        context = super().get_context_data(**kwargs)
        context.update({
            "similar_post": similar_post,
            'form':self.form,
            "product_review":product_review,
            "product": product,
            'product_reviews_count': product_review_count
        })
        
        return context
    


class SignupPage(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'signup.html')
        
        
    def post(self, *args, **kwargs):
        username = self.request.POST['username']  
        email = self.request.POST['email']
        password = self.request.POST['password']
        password2 = self.request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(self.request, "Email Taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(self.request, "Username taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                user_login = auth.authenticate(username=username, password=password)
                auth.login(self.request, user_login)                
                return redirect('/')
        else:
            messages.info(self.request, "password doesnt match")
            return redirect('signup')
        
class SigninPage(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'signin.html')
        
    def post(self, *args, **kwargs):
        username = self.request.POST['username']
        password = self.request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(self.request, user)
            return redirect('/')
        else:
            messages.info(self.request, "Invalid Credentials")
            return redirect('signin')
            

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
