#django
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import the_applications.func as f
from django.contrib.auth.models import User
from the_applications.notify.models import TypeNotify, Notify
from django.shortcuts import render, redirect
from the_applications.notify.forms import TypeNotifyForm
from the_applications.notify.forms import NotifyForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
import json
import the_applications.func as f
from datetime import datetime, timezone
import timeago
# Model

class Principal(LoginRequiredMixin, TemplateView):
    template_name = 'notify/main.html'

    def get_context_data(self, **kwargs):
        context2 = super().get_context_data(**kwargs)
        users = User.objects.all().values()
        type_notify = TypeNotify.objects.all().filter(active=True).values()
        users_array = []
        type_array = []
        for user in users:
            item = {
                'id': user['id'],
                'username': user['username']
            }
            users_array.append(item)
        for type in type_notify:
            item = {
                'id': type['id'],
                'name': type['name']
            }
            type_array.append(item)
        context2['context'] = {
            "users" : users_array,
            "type_notify" : type_array
        }


        return context2

class Type(LoginRequiredMixin, TemplateView):
    template_name = 'notify/type.html'

    def get_context_data(self, **kwargs):
        context2 = super().get_context_data(**kwargs)
        users = User.objects.all().values()
        type_notify = TypeNotify.objects.all().values()
        users_array = []
        type_array = []
        for user in users:
            item = {
                'id': user['id'],
                'username': user['username']
            }
            users_array.append(item)
        for type in type_notify:
            item = {
                'id': type['id'],
                'name': type['name']
            }
            type_array.append(item)
        context2['context'] = {
            "users" : users_array,
            "type_notify" : type_array
        }


        return context2
class Inbox(LoginRequiredMixin, TemplateView): # ----------- ok
    template_name = 'notify/inbox.html'

    def get_context_data(self, **kwargs):
        context2 = super().get_context_data(**kwargs)
        users = User.objects.all().values()
        type_notify = TypeNotify.objects.all().values()
        users_array = []
        type_array = []
        for user in users:
            item = {
                'id': user['id'],
                'username': user['username']
            }
            users_array.append(item)
        for type in type_notify:
            item = {
                'id': type['id'],
                'name': type['name']
            }
            type_array.append(item)
        context2['context'] = {
            "users" : users_array,
            "type_notify" : type_array
        }

        query = Notify.objects.filter(user_id=self.request.user.id).values('type_id').annotate(
            dcount=Count('type_id')).order_by()
        etiqueta = []
        for q in query:
            xquery = TypeNotify.objects.filter(pk=q['type_id']).values()
            for xq in xquery:
                etiqueta.append({'name': xq['name'], 'color': xq['color'], 'id': xq['id']})

        context2['etiqueta'] = etiqueta
        context2['user_id'] = self.request.user.id

        return context2

class New(LoginRequiredMixin, TemplateView):
    template_name = 'notify/new.html'

    def get_context_data(self, **kwargs):
        context2 = super().get_context_data(**kwargs)
        users = User.objects.all().values()
        type_notify = TypeNotify.objects.all().values()
        users_array = []
        type_array = []
        for user in users:
            item = {
                'id': user['id'],
                'username': user['username']
            }
            users_array.append(item)
        for type in type_notify:
            item = {
                'id': type['id'],
                'name': type['name']
            }
            type_array.append(item)
        context2['context'] = {
            "users" : users_array,
            "type_notify" : type_array
        }

        query = Notify.objects.filter(user_id=self.request.user.id).values('type_id').annotate(
            dcount=Count('type_id')).order_by()
        etiqueta = []
        for q in query:
            xquery = TypeNotify.objects.filter(pk=q['type_id']).values()
            for xq in xquery:
                etiqueta.append({'name': xq['name'], 'color': xq['color'], 'id': xq['id']})

        context2['etiqueta'] = etiqueta

        return context2


class CreateTypeNotify(LoginRequiredMixin, TemplateView):
    template_name = 'notify/main.html'


    def post(self, request, *args, **kwargs):
        context = {}
        data=request.POST
        form = TypeNotifyForm(data)
        if form.is_valid():
            form.save()
            return redirect('notify:panel')
        else:
            pass
        context['form'] = form
        context['active_type_notify'] = True
        return render(
            request,
            'notify/main.html',
            context,
        )

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2

class DatatablesTypeNotify(LoginRequiredMixin, TemplateView):
    template_name = 'notify/main.html'


    def post(self, request, *args, **kwargs):
        query = TypeNotify.objects.all().values()
        response = {
            'data':[],
            'error': False,
            'msj':''
        }
        data = []
        for q in query:
            item = {
                'id':q["id"],
                'name':q['name'],
                'color':q['color'],
                'description':q['description'],
                'active':q['active'],
                'created':q['created'].strftime("%m/%d/%Y %H:%M:%S"),
                'modified':q['modified'].strftime("%m/%d/%Y %H:%M:%S"),
            }
            data.append(item)
        response['data']=data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2
class DatatablesNotifyInbox(LoginRequiredMixin, TemplateView):
    template_name = 'notify/inbox.html'


    def post(self, request, *args, **kwargs):
        query = Notify.objects.filter(user_id=request.user.id, active=1, important=0, trash=0).values()
        response = {
            'data':[],
            'error': False,
            'msj':''
        }
        data = []
        for q in query:
            item = {
                'id': q['id'],
                'user': User.objects.get(pk=q['user_id']).username,
                'type': TypeNotify.objects.get(pk=q['type_id']).name,
                'name': q['name'],
                'description': q['description'],
                'priority': q['priority'],
                'picture': q['picture'],
                'created': q['created'].strftime("📆%m/%d/%Y 🕝%H:%M:%S"),
                'modified': q['modified'].strftime("📆%m/%d/%Y 🕝%H:%M:%S"),
                'active': q['active'],
                'see': q['see'],
                'to': User.objects.get(pk=q['to']).username,
                'colortype': TypeNotify.objects.get(pk=q['type_id']).color
            }
            data.append(item)
        response['data'] = data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2
class DatatablesNotifyImportant(LoginRequiredMixin, TemplateView):
    template_name = 'notify/important.html'

    def post(self, request, *args, **kwargs):
        query = Notify.objects.filter(user_id=request.user.id, active=1, important=1, trash=0).values()
        response = {
            'data':[],
            'error': False,
            'msj':''
        }
        data = []
        for q in query:
            item = {
                'id': q['id'],
                'user': User.objects.get(pk=q['user_id']).username,
                'type': TypeNotify.objects.get(pk=q['type_id']).name,
                'name': q['name'],
                'description': q['description'],
                'priority': q['priority'],
                'picture': q['picture'],
                'created': q['created'].strftime("📆%m/%d/%Y 🕝%H:%M:%S"),
                'modified': q['modified'].strftime("📆%m/%d/%Y 🕝%H:%M:%S"),
                'active': q['active'],
                'see': q['see'],
                'to': User.objects.get(pk=q['to']).username,
                'colortype': TypeNotify.objects.get(pk=q['type_id']).color
            }
            data.append(item)
        response['data'] = data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2

class DatatablesNotifyTrash(LoginRequiredMixin, TemplateView):
    template_name = 'notify/trash.html'

    def post(self, request, *args, **kwargs):
        query = Notify.objects.filter(user_id=request.user.id, active=1, trash=1).values()
        response = {
            'data':[],
            'error': False,
            'msj':''
        }
        data = []
        for q in query:
            item = {
                'id': q['id'],
                'user': User.objects.get(pk=q['user_id']).username,
                'type': TypeNotify.objects.get(pk=q['type_id']).name,
                'name': q['name'],
                'description': q['description'],
                'priority': q['priority'],
                'picture': q['picture'],
                'created': q['created'].strftime("📆%m/%d/%Y 🕝%H:%M:%S"),
                'modified': q['modified'].strftime("📆%m/%d/%Y 🕝%H:%M:%S"),
                'active': q['active'],
                'see': q['see'],
                'to': User.objects.get(pk=q['to']).username,
                'colortype': TypeNotify.objects.get(pk=q['type_id']).color
            }
            data.append(item)
        response['data'] = data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2


class DatatablesNotifySend(LoginRequiredMixin, TemplateView):
    template_name = 'notify/send.html'

    def post(self, request, *args, **kwargs):
        query = Notify.objects.filter(user_id=request.user.id).values()
        response = {
            'data':[],
            'error': False,
            'msj':''
        }
        data = []
        for q in query:
            item = {
                'id': q['id'],
                'user': User.objects.get(pk=q['user_id']).username,
                'type': TypeNotify.objects.get(pk=q['type_id']).name,
                'name': q['name'],
                'description': q['description'],
                'priority': q['priority'],
                'picture': q['picture'],
                'created': q['created'].strftime("📆%m/%d/%Y 🕝%H:%M:%S"),
                'modified': q['modified'].strftime("📆%m/%d/%Y 🕝%H:%M:%S"),
                'active': q['active'],
                'see': q['see'],
                'to': User.objects.get(pk=q['to']).username,
                'colortype': TypeNotify.objects.get(pk=q['type_id']).color
            }
            data.append(item)
        response['data'] = data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2

class CreateNotify(LoginRequiredMixin, TemplateView):
    template_name = 'notify/main.html'


    def post(self, request, *args, **kwargs):
        context = {}
        d = {
            'user': '',
            'type': '',
            'name': '',
            'description': '',
            'priority': '',
            'picture': '',
            'from': ''
        }

        d['from'] = request.user.id
        data = request.POST
        d['user'] =int(data['user'])
        d['type'] = int(data['type'])
        d['name'] = data['name']
        d['description'] = data['description']
        d['priority'] = int(data['priority'])
        if request.FILES:
            file = request.FILES
            d['picture'] = file['picture']
        form = NotifyForm(data)
        if form.is_valid():
            form.save(d)
            return redirect('notify:panel')
        else:
            context['name_app'] = "Roadly"
            context['info_app'] = "Ruteador de Raloy"
            users = User.objects.all().values()
            type_notify = TypeNotify.objects.all().values()
            users_array = []
            type_array = []
            for user in users:
                item = {
                    'id': user['id'],
                    'username': user['username']
                }
                users_array.append(item)
            for type in type_notify:
                item = {
                    'id': type['id'],
                    'name': type['name']
                }
                type_array.append(item)
            context['context'] = {
                "users": users_array,
                "type_notify": type_array
            }
        context['form'] = form
        context['active_notify'] = True
        return render(
            request,
            'notify/main.html',
            context,
        )

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2

class DatatablesNotify(LoginRequiredMixin, TemplateView):
    template_name = 'notify/main.html'


    def post(self, request, *args, **kwargs):
        query = Notify.objects.all().values()
        response = {
            'data':[],
            'error': False,
            'msj':''
        }
        data = []
        for q in query:
            item = {
                'id': q['id'],
                'user': User.objects.get(pk=q['user_id']).username,
                'type': TypeNotify.objects.get(pk=q['type_id']).name,
                'name': q['name'],
                'description': q['description'],
                'priority': q['priority'],
                'picture': q['picture'],
                'created':q['created'].strftime("%m/%d/%Y %H:%M:%S"),
                'modified':q['modified'].strftime("%m/%d/%Y %H:%M:%S"),
                'active': q['active'],
                'see': q['see'],
                'to': User.objects.get(pk=q['to']).username,
                'colortype': TypeNotify.objects.get(pk=q['type_id']).color
            }
            data.append(item)
        response['data']=data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2


@login_required
def ShowId(request):
    idNotify = request.GET['id']
    notify = Notify.objects.get(pk=idNotify)
    notify.see = 1
    notify.modified = datetime.now(timezone.utc)
    notify.save()
    notify = Notify.objects.filter(pk=idNotify).values()
    nitem = {}
    for n in notify:
        print(n)
        now = datetime.now(timezone.utc)
        now = now.replace(tzinfo=None)
        zdate = n['created'].replace(tzinfo=None)
        bages = []
        if n['priority'] == 1:
            bitem = {'name':'Alta', 'color':'#00acac'}
            bages.append(bitem)
        elif n['priority'] == 2:
            bitem = {'name':'Media', 'color':'#f59c1a'}
            bages.append(bitem)
        elif n['priority'] == 3:
            bitem = {'name':'Baja', 'color':'#b6b6b6'}
            bages.append(bitem)
        else:
            bitem = {'name':'Unknown', 'color':'#b6b6b6'}
            bages.append(bitem)
        btype = {'name':TypeNotify.objects.filter(pk=n['type_id']).values('name')[0]['name'], 'color':TypeNotify.objects.filter(pk=n['type_id']).values('color')[0]['color']}
        bages.append(btype)
        if n['see'] == 1:
            bsee = {'name':'Visto', 'color':'#00af62'}
            bages.append(bsee)
        if n['important'] == 1:
            bimportant = {'name':'Importante', 'color':'#f44336'}
            bages.append(bimportant)
        if n['trash'] == 1:
            bimportant = {'name':'Basurero', 'color':'#818181'}
            bages.append(bimportant)
        if n['active'] == 0:
            bimportant = {'name':'Correo archivado, no visible', 'color':'#ff0000'}
            bages.append(bimportant)
        f.aqui_ando(n=1111, t=bages)
        nitem = {
            'title': n['name'],
            'img': n['picture'],
            'from': "De : {}<{}>".format(User.objects.filter(pk=n['to']).values('username')[0]['username'],User.objects.filter(pk=n['to']).values('email')[0]['email']),
            'date': "{} - {}".format(timeago.format(now.strftime("%Y-%m-%d %H:%M:%S"), zdate.strftime("%Y-%m-%d %H:%M:%S")), zdate.strftime("%Y-%m-%d %H:%M:%S")),
            'to': 'Para : {}<{}>'.format(User.objects.filter(pk=n['user_id']).values('username')[0]['username'],User.objects.filter(pk=n['user_id']).values('email')[0]['email']),
            'message': n['description'],
            'badge': bages,
            'id': n['id'],
            'modified': n['modified'].replace(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")
        }

    query = Notify.objects.filter(user_id=request.user.id).values('type_id').annotate(dcount=Count('type_id')).order_by()
    etiqueta = []
    for q in query:
        xquery = TypeNotify.objects.filter(pk=q['type_id']).values()
        for xq in xquery:
            etiqueta.append({'name': xq['name'], 'color': xq['color'], 'id':xq['id']})
    context = {
        'etiqueta' : etiqueta,
        'notify' : nitem
    }

    return render(
        request=request,
        template_name='notify/show.html',
        context=context
    )


@login_required
def LabelShow(request):
    idLabel = request.GET['id']
    idUser = request.GET['user']
    notify = Notify.objects.filter(type=idLabel, to=idUser, active=True, trash=False).values()
    nitem = []
    
    context = {
        'notify' : nitem
    }

    return render(
        request=request,
        template_name='notify/show.html',
        context=context
    )

class PostChangeImportant(LoginRequiredMixin, TemplateView):
    template_name = 'notify/show.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = request.POST['id']
        notify = Notify.objects.get(pk=id)
        notify.modified = datetime.now(timezone.utc)
        f.aqui_ando(t=notify.important)
        if notify.important == 0:
            notify.important = 1
            response['msj'] = 'Se ha marcado la notificación como Importante'
        else:
            notify.important = 0
            response['msj'] = 'Se ha desmarcado la notificación como Importante'
        notify.save()
        response['notify'] = notify.id
        return JsonResponse(response)


class PostChangeTrash(LoginRequiredMixin, TemplateView):
    template_name = 'notify/show.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = request.POST['id']
        notify = Notify.objects.get(pk=id)
        notify.modified = datetime.now(timezone.utc)
        f.aqui_ando(t=notify.trash)
        if notify.trash == 0:
            notify.trash = 1
            response['msj'] = 'Se ha marcado la notificación como Basura'
        else:
            notify.trash = 0
            response['msj'] = 'Se ha desmarcado la notificación como Basura'
        notify.save()
        response['notify'] = notify.id
        return JsonResponse(response)

class PostChangeActive(LoginRequiredMixin, TemplateView):
    template_name = 'notify/show.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = request.POST['id']
        notify = Notify.objects.get(pk=id)
        notify.modified = datetime.now(timezone.utc)
        f.aqui_ando(t=notify.active)
        notify.active = 0
        response['msj'] = 'Se ha archivado la notificación, si requiere verla nuevamente comuniquese con su administrador'
        notify.save()
        response['notify'] = notify.id
        return JsonResponse(response)

class PostChangeDeactive(LoginRequiredMixin, TemplateView):
    template_name = 'notify/show.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = request.POST['id']
        notify = Notify.objects.get(pk=id)
        notify.modified = datetime.now(timezone.utc)
        f.aqui_ando(t=notify.active)
        notify.active = 1
        response['msj'] = 'Se ha desarchivado la notificación.'
        notify.save()
        response['notify'] = notify.id
        return JsonResponse(response)

class PostChangeActiveType(LoginRequiredMixin, TemplateView):
    template_name = 'notify/show.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = request.POST['id']
        notify = TypeNotify.objects.get(pk=id)
        notify.modified = datetime.now(timezone.utc)
        f.aqui_ando(t=notify.active)
        notify.active = 0
        response['msj'] = 'Se ha archivado el tipo de notificación'
        notify.save()
        response['notify'] = notify.id
        return JsonResponse(response)

class PostChangeDeactiveType(LoginRequiredMixin, TemplateView):
    template_name = 'notify/show.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = request.POST['id']
        notify = TypeNotify.objects.get(pk=id)
        notify.modified = datetime.now(timezone.utc)
        f.aqui_ando(t=notify.active)
        notify.active = 1
        response['msj'] = 'Se ha desarchivado el tipo de notificación.'
        notify.save()
        response['notify'] = notify.id
        return JsonResponse(response)

class GetNotifyInbox(LoginRequiredMixin, TemplateView):
    template_name = 'notify/inbox.html'

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

class GetNotifyImportant(LoginRequiredMixin, TemplateView):
    template_name = 'notify/important.html'

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

    def get_context_data(self, **kwargs):
        context2 = super().get_context_data(**kwargs)
        query = Notify.objects.filter(user_id=self.request.user.id).values('type_id').annotate(
            dcount=Count('type_id')).order_by()
        etiqueta = []
        for q in query:
            xquery = TypeNotify.objects.filter(pk=q['type_id']).values()
            for xq in xquery:
                etiqueta.append({'name': xq['name'], 'color': xq['color'], 'id': xq['id']})

        context2['etiqueta'] = etiqueta
        context2['user_id'] = self.request.user.id
        return context2


class GetNotifyTrash(LoginRequiredMixin, TemplateView):
    template_name = 'notify/trash.html'

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

    def get_context_data(self, **kwargs):
        context2 = super().get_context_data(**kwargs)
        query = Notify.objects.filter(user_id=self.request.user.id).values('type_id').annotate(
            dcount=Count('type_id')).order_by()
        etiqueta = []
        for q in query:
            xquery = TypeNotify.objects.filter(pk=q['type_id']).values()
            for xq in xquery:
                etiqueta.append({'name': xq['name'], 'color': xq['color'], 'id': xq['id']})

        context2['etiqueta'] = etiqueta
        context2['user_id'] = self.request.user.id
        return context2


class GetNotifySend(LoginRequiredMixin, TemplateView):
    template_name = 'notify/send.html'

    def post(self, request, *args, **kwargs):
        ### --------- NOTIFICACIÓN ------------- ###
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        noti = Notify.objects.filter(user_id=request.user.id, active=True).values()
        f.aqui_ando(9999999999999,t=noti)
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

    def get_context_data(self, **kwargs):
        context2 = super().get_context_data(**kwargs)
        query = Notify.objects.filter(user_id=self.request.user.id).values('type_id').annotate(
            dcount=Count('type_id')).order_by()
        etiqueta = []
        for q in query:
            xquery = TypeNotify.objects.filter(pk=q['type_id']).values()
            for xq in xquery:
                etiqueta.append({'name': xq['name'], 'color': xq['color'], 'id': xq['id']})

        context2['etiqueta'] = etiqueta
        context2['user_id'] = self.request.user.id
        return context2
