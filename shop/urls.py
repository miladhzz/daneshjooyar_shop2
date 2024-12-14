from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('store', views.Store.as_view(), name="store"),
    path('<int:id>/<str:title>/', views.Detail.as_view(), name="detail"),
]
