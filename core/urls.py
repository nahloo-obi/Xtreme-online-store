from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"), 
    path('shop-page', views.shopPage, name='shop-page'),
    path('menshop-page', views.menPage, name='menshop-page'),
    path('womenshop-page', views.womenPage, name='womenshop-page'),
    path('cart-page/<str:pk>', views.cartPage, name='cart-page'),
    path('add-to-cart/<str:pk>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<str:pk>/<str:size>/<str:colour>', views.remove_from_cart, name='remove-from-cart'),
    path('add-single-quantity/<str:pk>/<str:size>/<str:colour>', views.add_singleQuantity_to_product, name='add-single-quantity'),
    path('remove-single-quantity/<str:pk>/<str:size>/<str:colour>', views.remove_singleQuantity_from_product, name='remove-single-quantity'),
    path('order-page', views.orderSummaryPage, name='order-page'),
    path('checkout-page', views.checkoutPage, name='checkout-page')
]
