from django.views.generic import ListView
from shop.models import Product, Category
from django.db.models import Count
from core.logger import logger
from django.utils import timezone


class SearchView(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        try:
            queryset = super().get_queryset()

            q = self.request.GET.get('q', '')
            category = self.request.GET.get('category', '')
            min_price = self.request.GET.get('min_price', '')
            max_price = self.request.GET.get('max_price', '')

            # لاگ کردن پارامترهای جستجو
            logger.info(
                f"درخواست جستجو - کاربر: {self.request.user.username if self.request.user.is_authenticated else 'مهمان'} - "
                f"عبارت: {q} - دسته‌بندی: {category} - "
                f"حداقل قیمت: {min_price} - حداکثر قیمت: {max_price}"
            )

            if q:
                queryset = queryset.filter(title__icontains=q).order_by('title')
            if category:
                queryset = queryset.filter(category__title=category).order_by('title')
            if min_price:
                queryset = queryset.filter(price__gte=min_price).order_by('title')
            if max_price:
                queryset = queryset.filter(price__lte=max_price).order_by('title')

            return queryset

        except Exception as e:
            logger.error(f"خطا در جستجو: {str(e)}")
            return Product.objects.none()

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.annotate(product_count=Count('product')).filter(product_count__gt=0)

            params = self.request.GET.copy()
            params.pop('page', None)
            context['current_params'] = params

            context['search_query'] = self.request.GET.get('q', '')
            context['selected_category'] = self.request.GET.get('category', '')
            context['min_price'] = self.request.GET.get('min_price', '')
            context['max_price'] = self.request.GET.get('max_price', '')
            
            return context
        except Exception as e:
            logger.error(f"خطا در آماده‌سازی داده‌های جستجو: {str(e)}")
            return {}
