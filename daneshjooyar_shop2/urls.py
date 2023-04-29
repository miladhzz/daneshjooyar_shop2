from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("website.urls", namespace="website")),
    path('shop/', include("shop.urls", namespace="shop")),
]
