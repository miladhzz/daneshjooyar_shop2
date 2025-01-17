from django.contrib.sitemaps import Sitemap
from shop.models import Product
from django.urls import reverse


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(status=True)

    def lastmod(self, obj):
        return obj.updated_at


class StaticViewSitemap(Sitemap):
    priority = 0.3
    changefreq = "yearly"

    def items(self):
        return ["shop:about", ]

    def location(self, item):
        return reverse(item)
