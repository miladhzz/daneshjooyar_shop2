from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, Cart, OrderProduct, Order
from accounts.models import User


@receiver(post_save, sender=Product)
def soft_delete_cart(sender, instance, created, **kwargs):
    if not created:
        product: Product = instance
        if product.deleted:
            carts = Cart.objects.filter(product=product)
            for cart in carts:
                cart.delete()


@receiver(post_save, sender=User)
def soft_delete_cart(sender, instance, created, **kwargs):
    if not created:
        user: User = instance
        if user.deleted:
            carts = Cart.objects.filter(user=user)
            for cart in carts:
                cart.delete()


@receiver(post_save, sender=Product)
def soft_delete_order_product(sender, instance, created, **kwargs):
    if not created:
        product: Product = instance
        if product.deleted:
            order_products = OrderProduct.objects.filter(product=product)
            for order_product in order_products:
                order_product.delete()


@receiver(post_save, sender=Order)
def soft_delete_order_product(sender, instance, created, **kwargs):
    if not created:
        order: Order = instance
        if order.deleted:
            order_products = OrderProduct.objects.filter(order=order)
            for order_product in order_products:
                order_product.delete()

@receiver(post_save, sender=User)
def soft_delete_order(sender, instance, created, **kwargs):
    if not created:
        user: User = instance
        if user.deleted:
            orders = Order.objects.filter(user=user)
            for order in orders:
                order.delete()
