from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('get-cities/', views.get_cities, name='get_cities'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('email-login/', views.EmailLogin.as_view(), name='email_login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('active-email/<str:encoded_user_id>/<str:token>/', views.ActiveEmail.as_view(), name='active_email'),
    path('mobile-login/', views.MobileLogin.as_view(), name='mobile_login'),
    path('verify-otp/', views.VerifyOtp.as_view(), name='verify_otp'),
    path('resend-otp/', views.ResendOtp.as_view(), name='resend_otp'),
]
