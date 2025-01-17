from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import views
from .sitemap import ProductSitemap, StaticViewSitemap

sitemaps = {
    'products': ProductSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include("website.urls", namespace="website")),
    path('', include("shop.urls", namespace="shop")),
    path('checkout/', include("checkout.urls", namespace="checkout")),
    path('discount/', include("discount.urls", namespace="discount")),
    path('payment/', include("payment.urls", namespace="payment")),
    path('accounts/', include("accounts.urls", namespace="accounts")),
    path(
      "sitemap.xml",
      views.index,
      {"sitemaps": sitemaps},
      name="django.contrib.sitemaps.views.index",
      ),
    path(
          "sitemap-<section>.xml",
          views.sitemap,
          {"sitemaps": sitemaps},
          name="django.contrib.sitemaps.views.sitemap",
      ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
