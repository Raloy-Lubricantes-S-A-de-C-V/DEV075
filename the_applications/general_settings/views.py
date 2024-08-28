from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from the_applications.notify.models import Notify, TypeNotify
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
import the_applications.func as f
from django.contrib.auth.models import User
from datetime import datetime, timezone
import timeago
from .models import ModelConfig

@login_required
def ping(request):
    context = {
        'name_app' : "Roadly",
        'info_app' : "Ruteador de Raloy"
    }
    return render(request, 'panel.html', context)

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


class GetNotify(LoginRequiredMixin, TemplateView):
    template_name = 'notify/main.html'

    def post(self, request, *args, **kwargs):
        ### --------- NOTIFICACIÓN ------------- ###
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        noti = Notify.objects.filter(user_id=request.user.id, active=True, see=False).values()
        f.aqui_ando(t=noti)
        notis = []
        for n in noti:
            now = datetime.now(timezone.utc)
            now = now.replace(tzinfo=None)
            zdate = n['modified'].replace(tzinfo=None)
            if n['priority'] == 1:
                p = {"type":"Alta", "color":"#00acac"}
            elif n['priority'] == 2:
                p = {"type":"Media", "color":"#f59c1a"}
            elif n['priority'] == 3:
                p = {"type":"Baja", "color":"#b6b6b6"}
            else:
                p = {"type":"Known", "color":"#b6b6b6"}
            item = {
                'user': User.objects.get(pk=n['user_id']).username,
                'type': TypeNotify.objects.get(pk=n['type_id']).name,
                'title': n['name'],
                'date': timeago.format(now.strftime("%Y-%m-%d %H:%M:%S"), zdate.strftime("%Y-%m-%d %H:%M:%S")),
                'img': n['picture'],
                'id': n['id'],
                'priority': p
            }
            notis.append(item)
        response['data'] = notis
        f.aqui_ando(n=2, t=response)
        return JsonResponse(response)
        ### --------- NOTIFICACIÓN ------------- ###