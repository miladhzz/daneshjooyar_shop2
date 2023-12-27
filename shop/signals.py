from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, Cart


@receiver(post_save, sender=Product)
def soft_delete_cart(sender, instance, created, **kwargs):
    if not created:
        product: Product = instance
        if product.deleted:
            carts = Cart.objects.filter(product=instance)
            for cart in carts:
                cart.delete()
