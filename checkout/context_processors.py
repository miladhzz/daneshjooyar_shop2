from .cart import Cart
from shop.models import Product
from decimal import Decimal


def cart(request):
    cart_session = Cart(request)
    if cart_session:
        product_ids = cart_session.product_ids
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_session[str(product.id)]['product'] = product

        all_total_price = 0
        cart_length = 0
        for item in cart_session:
            item['total_price'] = Decimal(item['price']) * item['quantity']
            all_total_price += item['total_price']
            cart_length += item['quantity']

        cart_session.all_total_price = all_total_price
        cart_session.cart_length = cart_length

        return {'cart': cart_session}

