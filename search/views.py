from django.views.generic import ListView
from shop.models import Product, Category
# این اضافه شد
from django.db.models import Count
from django.db.models import Q
from django.urls import reverse



class SearchView(ListView):  
    model = Product  
    template_name = 'search.html'  
    context_object_name = 'products'  
    paginate_by = 3  

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        context['categories'] = self.get_categories()  
        context['current_params'] = self.get_current_params()  
        context.update(self.get_search_parameters())  
        return context  

    def get_categories(self):  
        return Category.objects.annotate(  
            product_count=Count('product')  
        ).filter(product_count__gt=0)  

    def get_current_params(self):  
        params = self.request.GET.copy()  
        params.pop('page', None)
        return params  

    def get_search_parameters(self):  
        return {  
            'search_query': self.request.GET.get('q', ''),  
            'selected_category': self.request.GET.get('category', ''),  
            'min_price': self.request.GET.get('min_price', ''),  
            'max_price': self.request.GET.get('max_price', ''),  
        }  

    def get_queryset(self):  
        queryset = super().get_queryset()  
        filters = self.get_filters()  
        return queryset.filter(**filters)  

    def get_filters(self):  
        filters = {}  
        q = self.request.GET.get('q')  
        category = self.request.GET.get('category')  
        min_price = self.request.GET.get('min_price')  
        max_price = self.request.GET.get('max_price')  

        if q:  
            filters['title__icontains'] = q  
        if category:  
            filters['category__title'] = category  
        if min_price:  
            filters['price__gte'] = min_price  
        if max_price:  
            filters['price__lte'] = max_price  

        return filters  
