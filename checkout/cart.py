from . import models
CART_SESSION_ID = 'cart'


class DbCart:
    def __init__(self, request):
        self.user_id = request.user.id

    @property
    def product_ids(self):
        return self.cart.keys()

    @property
    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def __getitem__(self, item):
        return self.cart[item]

    def __iter__(self):
        for item in models.Cart.objects.filter(user_id=self.user_id):
            yield {
                'product_id': item.product.id,
                'quantity': item.quantity,
                'price': item.product.get_price,
                'product': item.product
            }

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


class SessionCart:
    def __init__(self, request):
        self.session = request.session

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


class Cart:
    @staticmethod
    def get_cart(request):
        if request.user.is_authenticated:
            return DbCart(request)
        else:
            return SessionCart(request)
