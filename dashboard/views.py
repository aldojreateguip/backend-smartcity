from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.backends import BaseBackend
from django.http import JsonResponse

def dashboard_view(request):

    return render(request, 'dashboard/dashboard.html')
