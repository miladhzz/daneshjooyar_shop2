from django.views import View
from django.views.generic import FormView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import Profile
from django.shortcuts import render, get_object_or_404, redirect, reverse
from core.models import Province
from .forms import OrderForm, AddToCartForm
from .utils import save_order_user, save_order_different
from .cart import Cart
from shop.models import Product
from django.urls import reverse_lazy
from django.http import Http404
import logging


class Checkout(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect(reverse('accounts:edit_profile') + '?next=' + reverse('checkout:checkout'))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'provinces': Province.objects.all()
        }
        return render(request, "checkout.html", context=context)

    def post(self, request, *args, **kwargs):
        cart = Cart.get_cart(request)
        different_address = request.POST.get('different_address')

        if different_address:
            order_form = OrderForm(request.POST)
            if not order_form.is_valid():
                logging.warning(f"Invalid order form for user {request.user.username}")
                return render(request, "checkout.html")
            
            order = save_order_different(cart, order_form, request)
            logging.info(f"New order with different address registered - Order: {order.id} - User: {request.user.username}")
            cart.clear()
            return redirect(reverse('payment:to_bank', args=[order.id]))

        order = save_order_user(cart, request)
        logging.info(f"New order with user address registered - Order: {order.id} - User: {request.user.username}")
        cart.clear()
        return redirect(reverse('payment:to_bank', args=[order.id]))


class AddToCart(FormView):
    form_class = AddToCartForm
    http_method_names = ['post']
    success_url = reverse_lazy('checkout:cart_detail')

    def form_valid(self, form):
        product_id = form.cleaned_data['product_id']
        quantity = form.cleaned_data['quantity']
        update = True if form.cleaned_data['update'] == 1 else False

        product = get_object_or_404(Product, id=product_id)
        cart = Cart.get_cart(self.request)
        cart.add(product_id, product.get_price, quantity, update)
        
        logging.info(f"Product added to cart - Product: {product.title} - Quantity: {quantity} - User: {self.request.user.username}")
        return redirect(self.get_success_url())


class CartDetail(TemplateView):
    template_name = 'cart_detail.html'


class RemoveFromCart(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)
            cart = Cart.get_cart(self.request)
            cart.remove(str(product_id))
            logging.info(f"Product removed from cart - Product: {product.title} - User: {request.user.username}")
            return redirect(reverse('checkout:cart_detail'))

        logging.warning(f"Attempt to remove non-existent product - Product ID: {product_id}")
        raise Http404('product is not found.')
