from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
# Create your views here.


class AplicacionesView(LoginRequiredMixin,TemplateView):
    template_name = 'notify/notify.html'