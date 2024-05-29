from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import City
from django.contrib.auth import authenticate, login as django_login


def edit_profile(request):
    return HttpResponse('<h1>Edit Profile</h1>')


def get_cities(request):
    province_id = request.GET.get('province_id')
    if not province_id:
        return JsonResponse({'error': 'province id is not valid!'}, status=400)

    cities = City.objects.filter(province_id=province_id).values('id', 'title')
    return JsonResponse(list(cities), safe=False)


def login(request):
    next_page = request.GET.get('next')
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return redirect(next_page)
        messages.error(request, 'Invalid username or password', 'danger')
        return render(request, 'login.html', {'form': form})

    return render(request, 'login.html', {'form': form})
