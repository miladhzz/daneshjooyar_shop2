from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import Profile
from django.shortcuts import render, redirect, reverse
from core.models import Province
from cart.models import Cart
from .forms import OrderForm
from .utils import save_order_different, save_order_user


class Checkout(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect(reverse('accounts:edit_profile') + '?next=' + reverse('shop:checkout'))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'provinces': Province.objects.all()
        }
        return render(request, "checkout.html", context=context)

    def post(self, request, *args, **kwargs):
        cart = Cart(request)

        different_address = request.POST.get('different_address')

        if different_address:
            order_form = OrderForm(request.POST)
            if not order_form.is_valid():
                return render(request, "checkout.html")
            order = save_order_different(cart, order_form, request)
            cart.clear()
            return redirect(reverse('shop:to_bank', args=[order.id]))

        # not different_address:
        order = save_order_user(cart, request)
        cart.clear()
        return redirect(reverse('shop:to_bank', args=[order.id]))
