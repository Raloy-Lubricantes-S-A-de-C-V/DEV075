from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ModelConfig

@login_required
def ping(request):
    pong = "Response 200 Ok"
    return render(request, 'panel.html', {'PING': pong})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')