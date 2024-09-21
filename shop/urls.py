from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('store', views.Store.as_view(), name="store"),
    path('checkout/', views.Checkout.as_view(), name="checkout"),
    path('to-bank/<int:order_id>/', views.ToBank.as_view(), name="to_bank"),
    path('verify/', views.Verify.as_view(), name="verify"),
    path('<int:id>/<str:title>/', views.Detail.as_view(), name="detail"),
    path('add-to-cart/', views.AddToCart.as_view(), name="add_to_cart"),
    path('cart/', views.CartDetail.as_view(), name="cart_detail"),
    path('cart/remove/<int:product_id>/', views.RemoveFromCart.as_view(), name="remove_from_cart"),
]
