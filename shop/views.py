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
    return render(request, "store.html")


def checkout(request):
    return render(request, "checkout.html")
