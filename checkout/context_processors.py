from .cart import Cart
from shop.models import Product
from decimal import Decimal
from .utils import sync_cart_db_to_session


def cart(request):
    session_cart = Cart.get_cart(request)
    if session_cart:

        if not request.user.is_authenticated:
            product_ids = session_cart.product_ids
            products = Product.objects.filter(id__in=product_ids)
            for product in products:
                session_cart[str(product.id)]['product'] = product

        all_total_price = 0
        cart_length = 0
        for item in session_cart:
            item['total_price'] = Decimal(item['price']) * item['quantity']
            all_total_price += item['total_price']
            cart_length += item['quantity']

        session_cart.all_total_price = all_total_price
        session_cart.cart_length = cart_length

        return {'cart': session_cart}


# def db_cart_context(request):
#     db_cart = Cart.get_cart(request)
#
#     all_total_price = 0
#     cart_length = 0
#
#     for item in db_cart:
#         item.total_price = Decimal(item.product.get_price * item.quantity)
#         all_total_price += item.total_price
#         cart_length += item.quantity
#
#     db_cart.all_total_price = all_total_price
#     db_cart.cart_length = cart_length
#
#     return {'cart': db_cart}
#
#
# def cart(request):
#     if request.user.is_authenticated:
#         return session_cart_context(request)
#     else:
#         return session_cart_context(request)
