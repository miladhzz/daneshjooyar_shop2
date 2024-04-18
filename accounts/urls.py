from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('edit-profile/', views.edit_profile, name="edit_profile"),
    path('get-cities/', views.get_cities, name="get_cities"),
]
