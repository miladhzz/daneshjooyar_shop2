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


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = LoginForm()
            return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        next_page = request.GET.get('next')
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_page if next_page else '/')
            messages.error(request, 'Invalid username or password', 'danger')
            return render(request, 'login.html', {'form': form})

        return render(request, 'login.html', {'form': form})


class EmailLogin(View):
    def get(self, request, *args, **kwargs):
        form = EmailLoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('shop:index'))
            messages.error(request, 'Invalid email or password', 'danger')
            return render(request, 'login.html', {'form': form})

        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('shop:index'))


class Register(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, 'register.html', {'form': form})

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        token = default_token_generator.make_token(user)
        encoded_user_id = urlsafe_base64_encode(force_bytes(user.id))
        activation_path = reverse('accounts:active_email', args=[encoded_user_id, token])
        activation_url = f'http://{current_site}{activation_path}'

        send_activation_code(activation_url, form.cleaned_data['email'])

        messages.info(request, 'An activation email has been sent to you. Please verify your email.')
        return redirect('accounts:login')


class ActiveEmail(View):
    def get(self, request, *args, **kwargs):
        try:
            user_id = force_str(urlsafe_base64_decode(kwargs.get('encoded_user_id')))
            user = User.objects.get(id=user_id, is_active=False)
        except (ValueError, User.DoesNotExist):
            return HttpResponse('<h1>Error, your request is invalid.</h1>')

        if not default_token_generator.check_token(user, kwargs.get('token')):
            return HttpResponse('<h1>Error, your activation link is invalid.</h1>')

        user.is_active = True
        user.save()
        return HttpResponse('<h1>Your account has been activated.</h1>')


class MobileLogin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mobile_login.html')

    def post(self, request, *args, **kwargs):
        mobile = request.POST.get('mobile')
        if mobile:
            request.session['mobile'] = mobile
            if cache.get(mobile):
                return redirect(reverse('accounts:verify_otp'))

            send_otp(mobile)
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
            User.objects.get_or_create(
                mobile=mobile,
                defaults={
                    'username': mobile,
                    'email': f'{mobile}@mail.com'
                }
            )
            user = authenticate(mobile=mobile)
            if user is not None:
                login(request, user)
                cache.delete(mobile)
                return redirect(reverse('shop:index'))

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
