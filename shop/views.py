from django.http import Http404
from django.shortcuts import render
from .models import Product, Order
from django.shortcuts import get_object_or_404, redirect, reverse
from .cart import Cart
from accounts.models import Profile, Province
from .forms import OrderForm
from django.conf import settings
import json
import requests
from django.views import View
from django.views.generic import ListView, DetailView
from .utility import save_order_user, save_order_different
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class Index(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'


class Detail(DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'id'


class Store(ListView):
    template_name = 'store.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = self.request.GET.get('category')

        if category:
            return Product.objects.filter(category__title=category)

        return Product.objects.all()


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


@method_decorator(login_required, name='dispatch')
class ToBank(View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id, user_id=request.user.id, status__isnull=True)
        data = {
            "MerchantID": settings.ZARINPAL_MERCHANT_ID,
            "Amount": order.total_price,
            "Description": f'sandbox, order: {order.id}',
            "CallbackURL": settings.ZARINPAL_CALLBACK_URL,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        try:
            response = requests.post(settings.ZARINPAL_REQUEST, data=data, headers=headers, timeout=10)
        except requests.exceptions.Timeout:
            return render(request, 'to_bank.html', {'error': 'time out error'})
        except requests.exceptions.ConnectionError:
            return render(request, 'to_bank.html', {'error': 'connection error'})

        if response.status_code != 200:
            return render(request, 'to_bank.html', {'error': f'response status code: {response.status_code}'})

        response = response.json()
        if response['Status'] != 100:
            return render(request, 'to_bank.html', {'error': f'status error code: {response["Status"]}'})

        authority = response['Authority']
        order.zarinpal_authority = authority
        order.status = False
        order.save()
        return redirect(settings.ZARINPAL_STARTPAY + authority)


class Verify(View):
    def get(self, request, *args, **kwargs):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')

        if not status or status != 'OK':
            return render(request, 'verify.html')

        order = get_object_or_404(Order, zarinpal_authority=authority)
        data = {
            "MerchantID": settings.ZARINPAL_MERCHANT_ID,
            "Amount": order.total_price,
            "Authority": order.zarinpal_authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        try:
            response = requests.post(settings.ZARINPAL_VERIFY, data=data, headers=headers, timeout=10)
        except requests.exceptions.Timeout:
            return render(request, 'verify.html', {'error': 'time out error'})
        except requests.exceptions.ConnectionError:
            return render(request, 'verify.html', {'error': 'connection error'})

        if response.status_code != 200:
            return render(request, 'verify.html', {'error': f'response status code: {response.status_code}'})

        response = response.json()
        if response['Status'] != 100:
            return render(request, 'verify.html', {'error': f'status error code: {response["Status"]}'})

        ref_id = response['RefID']
        order.zarinpal_ref_id = ref_id
        order.status = True
        order.save()
        return render(request, 'verify.html', {'ref_id': ref_id})


class AddToCart(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        update = True if request.POST.get('update') == '1' else False

        product = get_object_or_404(Product, id=product_id)

        cart = Cart(request)
        cart.add(product_id, product.price, int(quantity), update)

        return redirect(reverse('shop:cart_detail'))


class CartDetail(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cart_detail.html')


class RemoveFromCart(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        if Product.objects.filter(id=product_id).exists():
            cart = Cart(request)
            cart.remove(str(product_id))
            return redirect(reverse('shop:cart_detail'))

        raise Http404('product is not found.')



