from .cart import Cart
from shop.models import Product
from decimal import Decimal


def cart(request):
    cart_object = Cart.get_cart(request)
    if cart_object:

        if not request.user.is_authenticated:
            product_ids = cart_object.product_ids
            products = Product.objects.filter(id__in=product_ids)
            for product in products:
                cart_object[str(product.id)]['product'] = product

        all_total_price = 0
        cart_length = 0
        for item in cart_object:
            item['total_price'] = Decimal(item['price']) * item['quantity']
            all_total_price += item['total_price']
            cart_length += item['quantity']

        cart_object.all_total_price = all_total_price
        cart_object.cart_length = cart_length

        return {'cart': cart_object}

