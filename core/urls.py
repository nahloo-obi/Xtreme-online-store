from django.urls import path
from . import views 


urlpatterns = [
    path('', views.index, name="index"), 
    path('shop-page', views.shopPage, name='shop-page'),
    path('gender-filter-page/<str:gender>', views.genderFilterPage, name='gender-filter-page'),
    path('sale-filter-page/<str:sale>', views.productSaleFilter, name='sale-filter-page'),
    
    path('filter-page/<str:sale>/', views.Filter, name='filter-page'),

    path('cart-page/<str:pk>', views.cartPage, name='cart-page'),
    path('add-to-cart/<str:pk>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<str:pk>/<str:size>/<str:colour>', views.remove_from_cart, name='remove-from-cart'),
    path('add-single-quantity/<str:pk>/<str:size>/<str:colour>', views.add_singleQuantity_to_product, name='add-single-quantity'),
    path('remove-single-quantity/<str:pk>/<str:size>/<str:colour>', views.remove_singleQuantity_from_product, name='remove-single-quantity'),
    path('order-page', views.orderSummaryPage, name='order-page'),
    path('checkout-page', views.checkoutPage, name='checkout-page'),
    path('payment-page', views.paymentPage, name='payment-page'),
    path('payment_complete', views.payment_complete, name='payment_complete'),
    path('signup', views.SignupPage.as_view(), name='signup'),
    path('signin', views.SigninPage.as_view(), name='signin'),
    path('logout', views.logout, name='logout'),
]
