from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('edit_profile/', views.edit_profile, name="edit_profile"),
]
