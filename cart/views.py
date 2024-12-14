from django.views.generic import View, FormView, TemplateView
from django.urls import reverse_lazy
from .cart import Cart
from django.shortcuts import redirect, reverse, get_object_or_404
from .forms import AddToCartForm
from django.http import Http404
from shop.models import Product


class AddToCart(FormView):
    form_class = AddToCartForm
    http_method_names = ['post']
    success_url = reverse_lazy('shop:cart_detail')

    def form_valid(self, form):
        product_id = form.cleaned_data['product_id']
        quantity = form.cleaned_data['quantity']
        update = True if form.cleaned_data['update'] == 1 else False

        product = get_object_or_404(Product, id=product_id)

        cart = Cart(self.request)
        cart.add(product_id, product.price, quantity, update)

        return redirect(self.get_success_url())


class CartDetail(TemplateView):
    template_name = 'cart_detail.html'


class RemoveFromCart(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        if Product.objects.filter(id=product_id).exists():
            cart = Cart(request)
            cart.remove(str(product_id))
            return redirect(reverse('shop:cart_detail'))

        raise Http404('product is not found.')
