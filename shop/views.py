from .models import Product
from django.views.generic import ListView, DetailView, TemplateView
import logging


class Index(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'


class Detail(DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        logging.info(f"Viewing product details: {obj.title}")
        return obj


class Store(ListView):
    template_name = 'store.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category:
            logging.info(f"Viewing products in category: {category}")
            return Product.objects.filter(category__title=category)
        return Product.objects.all()


class About(TemplateView):
    template_name = 'about.html'
