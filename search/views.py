from django.views.generic import ListView
from shop.models import Product, Category
# این اضافه شد
from django.db.models import Count



class SearchView(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Product.objects.filter(title__icontains=query).order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = Category.objects.all()  اول این
        # بعد این اضافه میشه
        context['categories'] = Category.objects.annotate(product_count=Count('product')).filter(product_count__gt=0)
        # که حذف شده های منطقی رو هندل نکرده
        return context
