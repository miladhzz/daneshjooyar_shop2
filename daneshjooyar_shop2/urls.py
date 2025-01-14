from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include("website.urls", namespace="website")),
    path('', include("shop.urls", namespace="shop")),
    path('checkout/', include("checkout.urls", namespace="checkout")),
    path('discount/', include("discount.urls", namespace="discount")),
    path('payment/', include("payment.urls", namespace="payment")),
    path('accounts/', include("accounts.urls", namespace="accounts")),
    path('captcha/', include('captcha.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
