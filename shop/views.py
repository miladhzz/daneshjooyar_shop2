from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404


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
