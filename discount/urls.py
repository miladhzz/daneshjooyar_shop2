from django.urls import path
from . import views

app_name = "discount"

urlpatterns = [
    path('apply-discount/', views.apply_discount, name="apply_discount"),
]
