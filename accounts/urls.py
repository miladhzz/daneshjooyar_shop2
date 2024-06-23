from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('get-cities/', views.get_cities, name='get_cities'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('active-email/<str:encoded_user_id>/<str:token>/', views.active_email, name='active_email'),
]
