from django.http import HttpResponse
from django.shortcuts import render

def edit_profile(request):
    return HttpResponse('<h1>Edit Profile</h1>')
