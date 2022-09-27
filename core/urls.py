from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"), 
    path('shop-page', views.shopPage, name='shop-page'),
    path('menshop-page', views.menPage, name='menshop-page'),
    path('womenshop-page', views.womenPage, name='womenshop-page'),
    path('cart-page/<str:pk>', views.cartPage, name='cart-page'),
    path('add-to-cart/<str:pk>', views.add_to_cart, name='add-to-art')
]
