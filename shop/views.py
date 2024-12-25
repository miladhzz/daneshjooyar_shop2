from .models import Product
from django.views.generic import ListView, DetailView


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
