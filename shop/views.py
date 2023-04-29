from django.shortcuts import render, redirect, reverse


def index(request):
    return redirect(reverse("shop:store"))
    # return render(request, "index.html")


def product(request):
    return render(request, "product.html")


def store(request):
    return render(request, "store.html")


def checkout(request):
    return render(request, "checkout.html")
