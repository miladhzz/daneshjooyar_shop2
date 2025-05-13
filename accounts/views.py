from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_GET
from .utility import send_otp, send_activation_code
from .forms import LoginForm, RegisterForm, EmailLoginForm
from .models import City, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.views import View
from django.views.generic import FormView
from core.logger import logger

@login_required
def edit_profile(request):
    return HttpResponse('<h1>Edit Profile</h1>')


@require_GET
def get_cities(request):
    province_id = request.GET.get('province_id')
    if not province_id:
        return JsonResponse({'error': 'province id is not valid!'}, status=400)

    cities = City.objects.filter(province_id=province_id).values('id', 'title')
    return JsonResponse(list(cities), safe=False)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            logger.info(f"Successful login for user {username}")
            next_page = self.request.GET.get('next')
            return redirect(next_page if next_page else '/')

        logger.warning(f"Failed login attempt for username {username}")
        messages.error(self.request, 'Invalid username or password', 'danger')
        return render(self.request, 'login.html', {'form': form})


class EmailLogin(FormView):
    template_name = 'login.html'
    form_class = EmailLoginForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(reverse('shop:index'))

        messages.error(self.request, 'Invalid email or password', 'danger')
        return render(self.request, 'login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        logger.info(f"User {request.user.username} logged out")
    logout(request)
    return redirect(reverse('shop:index'))


class Register(FormView):
    template_name = 'register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        logger.info(f"New user registration: {user.username} with email {user.email}")

        current_site = get_current_site(self.request)
        token = default_token_generator.make_token(user)
        encoded_user_id = urlsafe_base64_encode(force_bytes(user.id))
        activation_path = reverse('accounts:active_email', args=[encoded_user_id, token])
        activation_url = f'http://{current_site}{activation_path}'

        send_activation_code(activation_url, form.cleaned_data['email'])
        logger.info(f"Activation email sent to user {user.username}")

        messages.info(self.request, 'An activation email has been sent to you. Please verify your email.')
        return redirect('accounts:login')


class ActiveEmail(View):
    def get(self, request, *args, **kwargs):
        try:
            user_id = force_str(urlsafe_base64_decode(kwargs.get('encoded_user_id')))
            user = User.objects.get(id=user_id, is_active=False)
        except (ValueError, User.DoesNotExist):
            logger.warning(f"Email activation error: Invalid user")
            return HttpResponse('<h1>Error, your request is invalid.</h1>')

        if not default_token_generator.check_token(user, kwargs.get('token')):
            logger.warning(f"Email activation error: Invalid token for user {user.username}")
            return HttpResponse('<h1>Error, your activation link is invalid.</h1>')

        user.is_active = True
        user.save()
        logger.info(f"User account {user.username} successfully activated")
        return HttpResponse('<h1>Your account has been activated.</h1>')


class MobileLogin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mobile_login.html')

    def post(self, request, *args, **kwargs):
        mobile = request.POST.get('mobile')
        if mobile:
            request.session['mobile'] = mobile
            if cache.get(mobile):
                logger.info(f"Request for resending verification code for mobile number {mobile}")
                return redirect(reverse('accounts:verify_otp'))

            send_otp(mobile)
            logger.info(f"Verification code sent to mobile number {mobile}")
            return redirect(reverse('accounts:verify_otp'))


class VerifyOtp(View):
    def get(self, request, *args, **kwargs):
        mobile = request.session.get('mobile')
        if not mobile:
            return redirect(reverse('accounts:mobile_login'))
        return render(request, 'verify_otp.html')

    def post(self, request, *args, **kwargs):
        mobile = request.session.get('mobile')
        if not mobile:
            return redirect(reverse('accounts:mobile_login'))

        otp = request.POST.get('otp')
        cached_otp = cache.get(mobile)
        if cached_otp and str(cached_otp) == otp:
            user, created = User.objects.get_or_create(
                mobile=mobile,
                defaults={
                    'username': mobile,
                    'email': f'{mobile}@mail.com'
                }
            )
            if created:
                logger.info(f"New user created with mobile number {mobile}")
            
            user = authenticate(mobile=mobile)
            if user is not None:
                login(request, user)
                logger.info(f"Successful login for user with mobile number {mobile}")
                cache.delete(mobile)
                return redirect(reverse('shop:index'))

        logger.warning(f"Invalid verification code for mobile number {mobile}")
        messages.error(request, 'Your otp is incorrect or yor user account is inactive', 'danger')
        return render(request, 'verify_otp.html')


class ResendOtp(View):
    def get(self, request, *args, **kwargs):
        mobile = request.session.get('mobile')

        if not mobile:
            return redirect(reverse('accounts:mobile_login'))

        if cache.get(mobile):
            return redirect(reverse('accounts:verify_otp'))

        send_otp(mobile)
        return redirect(reverse('accounts:verify_otp'))
