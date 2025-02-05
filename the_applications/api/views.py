# django
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import the_applications.func as f
from django.contrib.auth.models import User
from django.db.models import Q
import datetime as dt
from django.db.models import Count

from the_applications.datasheet.forms import CreateDataList, CopyDataList, FusionDataList
from the_applications.datasheet.models import Header as Cab, DataSheet as List, TempNextCode as Next, RelParent as Parent
from the_applications.notify.models import TypeNotify, Notify
from django.http import HttpResponse, JsonResponse


class Principal(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'company': 'Raloy Lubricantes',
            'api': 'v1',
            'application': 'roadly',
            'last_run': '01/01/2025',
            'server': 'test'
        }
        return JsonResponse(response)

    def get(self, request, *args, **kwargs):
        response = {
            'company': 'Raloy Lubricantes',
            'api': 'v1',
            'application': 'roadly',
            'last_run': '01/01/2025',
            'server': 'test'
        }
        return JsonResponse(response)

class Epicor01(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        context2 = {
            'erros': []
        }
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        return response