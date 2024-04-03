from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import Product
from django.shortcuts import get_object_or_404, redirect, reverse
from .cart import Cart


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


def checkout(request):
    return render(request, "checkout.html")


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
