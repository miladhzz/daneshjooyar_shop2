from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('get-cities/', views.get_cities, name='get_cities'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('active-email/<str:encoded_user_id>/<str:token>/', views.active_email, name='active_email'),
    path('mobile-login/', views.mobile_login, name='mobile_login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
]
