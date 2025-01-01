from .utils import sync_cart_session_to_db
from . import models
CART_SESSION_ID = 'cart'


class SessionCart:
    def __init__(self, request):
        self.session = request.session
        self.request = request

        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    @property
    def product_ids(self):
        return self.cart.keys()

    @property
    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def __getitem__(self, item):
        return self.cart[item]

    def __iter__(self):
        for item in self.cart.values():
            yield item

    def add(self, product_id, product_price, quantity, update):
        if product_id not in self.cart:
            self.cart[product_id] = {
                'product_id': product_id,
                'quantity': 0,
                'price': product_price
            }

        if update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.__save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.__save()

    def __save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.session.modified = True


class DbCart:

    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.total_price = None

    @property
    def product_ids(self):
        user_id = self.request.user.id
        return models.Cart.objects.filter(user_id=user_id).values('product_id')

    @property
    def get_total_price(self):
        user_id = self.request.user.id
        return sum(item.product.get_price * item.quantity for item in models.Cart.objects.filter(user_id=user_id))

    def __getitem__(self, item):
        user_id = self.request.user.id
        return models.Cart.objects.get(user_id=user_id, product_id=item)

    def __iter__(self):
        user_id = self.request.user.id
        for item in models.Cart.objects.filter(user_id=user_id):
            yield item

    def add(self, product_id, product_price, quantity, update):
        user_id = self.request.user.id
        session_key = self.request.session.session_key

        cart_db, created = models.Cart.objects.get_or_create(
            user_id=user_id,
            product_id=product_id,
            defaults={
                'quantity': quantity,
                'session_key': session_key
            }
        )
        if not created:
            cart_db.quantity = quantity
            cart_db.session_key = session_key
            cart_db.save()

    def remove(self, product_id):
        user_id = self.request.user.id
        models.Cart.objects.filter(user_id=user_id, product_id=product_id).delete()

    def clear(self):
        user_id = self.request.user.id
        models.Cart.objects.filter(user_id=user_id).delete()


class Cart:
    @staticmethod
    def get_cart(request):
        if request.user.is_authenticated:
            return DbCart(request)
        else:
            return SessionCart(request)
