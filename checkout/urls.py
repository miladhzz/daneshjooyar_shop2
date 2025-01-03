from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path('', views.Checkout.as_view(), name="checkout"),
    path('add-to-cart/', views.AddToCart.as_view(), name="add_to_cart"),
    path('cart/', views.CartDetail.as_view(), name="cart_detail"),
    path('cart/remove/<int:product_id>/', views.RemoveFromCart.as_view(), name="remove_from_cart"),
]
