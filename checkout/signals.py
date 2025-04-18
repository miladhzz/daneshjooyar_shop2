from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from shop.models import Product
from .models import Order, OrderProduct, Cart
from accounts.models import User, Profile
from .cart import SessionCart


@receiver(user_logged_in)
def sync_session_with_db(sender, request, user, **kwargs):
    cart = SessionCart(request)

    for item in cart:
        Cart.objects.get_or_create(
            user_id=user.id,
            product_id=item['product_id'],
            defaults={
                'quantity': item['quantity']
            }
        )


@receiver(post_save, sender=Product)
def soft_delete_cart(sender, instance, created, **kwargs):
    if not created:
        product: Product = instance
        if product.deleted:
            carts = Cart.objects.filter(product=product)
            for cart in carts:
                cart.delete()

            order_products = OrderProduct.objects.filter(product=product)
            for order_product in order_products:
                order_product.delete()


@receiver(post_save, sender=User)
def soft_delete_cart(sender, instance, created, **kwargs):
    if not created:
        user: User = instance
        if user.deleted:
            carts = Cart.objects.filter(user=user)
            for cart in carts:
                cart.delete()

            try:
                Profile.objects.get(user=user).delete()
            except Profile.DoesNotExist:
                pass

            orders = Order.objects.filter(user=user)
            for order in orders:
                order.delete()


@receiver(post_save, sender=Order)
def soft_delete_order_product(sender, instance, created, **kwargs):
    if not created:
        order: Order = instance
        if order.deleted:
            order_products = OrderProduct.objects.filter(order=order)
            for order_product in order_products:
                order_product.delete()
