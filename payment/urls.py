from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('to-bank/<int:order_id>/', views.ToBank.as_view(), name="to_bank"),
    path('verify/', views.Verify.as_view(), name="verify"),
]
