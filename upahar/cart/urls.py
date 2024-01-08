
from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart_summary,name="cart_summary"),
    path('add/',views.cart_add,name="cart_add"),
    path('delete/',views.cart_delete,name="cart_delete"),
    path('update/',views.cart_update,name="cart_update"),
    path('checkout/',views.checkout_view,name="checkout_view"),
    path('checkout/confirmation/',views.order_confirmation,name="order_confirmation"),
    path('checkout/verify/',views.verify_khalti,name="verify"),
    path('checkout/initiate/',views.init_khalti,name="initiate"),
    path('myorders/',views.my_orders,name="my_orders"),
]