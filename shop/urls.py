from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('', views.index, name="index"),
    path('store', views.store, name="store"),
    path('checkout/', views.checkout, name="checkout"),
    path('to-bank/<int:order_id>/', views.to_bank, name="to_bank"),
    path('verify/', views.verify, name="verify"),
    path('<int:id>/<str:title>/', views.detail, name="detail"),
    path('add-to-cart/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart_detail, name="cart_detail"),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name="remove_from_cart"),
]
