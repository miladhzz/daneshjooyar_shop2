from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import Product, Order, OrderProduct
from django.shortcuts import get_object_or_404, redirect, reverse
from .cart import Cart
from accounts.models import Profile, Province, City
from .forms import OrderForm


def index(request):
    products = Product.objects.all()
    return render(request, "index.html", {'products': products})


def detail(request, id:int, title:str):
    product = get_object_or_404(Product, id=id)
    context = {'product': product}
    return render(request, "detail.html", context)


def store(request):
    category = request.GET.get('category')

    if category is not None:
        products = Product.objects.filter(category__title=category)
        return render(request, "store.html", {'products': products})

    products = Product.objects.all()
    return render(request, "store.html", {'products': products})


@login_required
def checkout(request):
    try:
        Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect(reverse('accounts:edit_profile') + '?next=' + reverse('shop:checkout'))

    cart = Cart(request)
    if request.method == 'POST':
        different_address = request.POST.get('different_address')

        if different_address:
            order_form = OrderForm(request.POST)
            if not order_form.is_valid():
                return render(request, "checkout.html")
            order = save_order_different(cart, order_form, request)
            cart.clear()
            return render(request, "order_detail.html", {'order': order})

        # not different_address:
        order = save_order_user(cart, request)
        cart.clear()
        return render(request, "order_detail.html", {'order': order})

    context = {
        'provinces': Province.objects.all(),
        'cities': City.objects.all(),
    }
    return render(request, "checkout.html", context=context)


def save_order_user(cart, request):
    order = Order.objects.create(
        user=request.user,
        total_price=cart.get_total_price,
        note=request.POST.get('note'),
        different_address=False,
        first_name=request.user.first_name,
        last_name=request.user.last_name,
        mobile=request.user.mobile,
        postal_code=request.user.profile.postal_code,
        address=request.user.profile.address,
    )
    for item in cart:
        OrderProduct.objects.create(order=order,
                                    product_id=item['product_id'],
                                    quantity=item['quantity'],
                                    price=item['price'])
    return order


def save_order_different(cart, order_form, request):
    order = Order.objects.create(
        user=request.user,
        total_price=cart.get_total_price,
        note=request.POST.get('note'),
        different_address=True,
        first_name=order_form.cleaned_data['first_name'],
        last_name=order_form.cleaned_data['last_name'],
        mobile=order_form.cleaned_data['mobile'],
        postal_code=order_form.cleaned_data['postal_code'],
        address=order_form.cleaned_data['address'],
    )
    for item in cart:
        OrderProduct.objects.create(order=order,
                                    product_id=item['product_id'],
                                    quantity=item['quantity'],
                                    price=item['price'])
    return order


@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    update = True if request.POST.get('update') == '1' else False

    product = get_object_or_404(Product, id=product_id)

    cart = Cart(request)
    cart.add(product_id, str(product.price), int(quantity), update)

    return redirect(reverse('shop:cart_detail'))


def cart_detail(request):
    return render(request, 'cart_detail.html')


def remove_from_cart(request, product_id):
    if Product.objects.filter(id=product_id).exists():
        cart = Cart(request)
        cart.remove(str(product_id))
        return redirect(reverse('shop:cart_detail'))

    raise Http404('product is not found.')
