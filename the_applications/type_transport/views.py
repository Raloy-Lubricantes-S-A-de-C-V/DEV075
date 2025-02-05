#django
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from the_applications.type_transport.forms import TypeTransoportForms as TTF
from the_applications.type_transport.models import Transport as T
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from the_applications.notify.models import TypeNotify, Notify
from django.contrib.auth.decorators import login_required
# Model

class Principal(LoginRequiredMixin, TemplateView):
    template_name = 'type_transport/main.html'

    def post(self, request, *args, **kwargs):
        context = {
            'erros': []
        }
        response = {
            'data':[],
            'error': False,
            'msj':''
        }
        data = request.POST
        form = TTF(data)
        if form.is_valid():
            name = data["name"]
            form.save(user=request.user.id)
            type_notify = TypeNotify.objects.get(pk=1)
            new_notify = Notify(
                user=request.user,
                type=type_notify,
                name="Nuevo modelo API - {}".format(str(name)),
                description="""
                                                       El usuario "{} {}"  ha generado un nuevo tipo de transporte 
                                                        con identificador "{}". Ya puede ser utilizado para los modelos 
                                                        de evaluación del sitema dentro de las condiciones.  
                                                       """.format(request.user.first_name,
                                                                  request.user.last_name,
                                                                  str(name)),
                priority=1,
                picture='notify/pictures/camion.png'
            )
            new_notify.save()
            response['msj'] = "Se ha registrado el nuevo transporte con éxito. Folio {}".format(name)
        else:
            response['error'] = True
            response['msj'] = str(form.errors)
        context['form'] = form
        context['response'] = response
        return render(
            request,
            'type_transport/main.html',
            context,
        )

    def get_context_data(self, **kwargs):
        context2 = super().get_context_data(**kwargs)
        form = TTF()
        context2['form1'] = form
        context2['name_model'] = "Tipo de transporte"
        return context2

class DataTablesInfo(LoginRequiredMixin, TemplateView):
    template_name = 'type_transport/main.html'


    def post(self, request, *args, **kwargs):

        query = T.objects.all().values()
        response = {
            'data':[],
            'error': False,
            'msj':''
        }
        data = []
        for q in query:
            item = {
                'id': q["id"],
                'name': q["name"],
                'volumen': q["volumen"],
                'capacity_pallet': q["capacity_pallet"],
                'active': q["active"],
            }
            data.append(item)
        response['data']=data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2


class UpdateModel(LoginRequiredMixin, TemplateView):
    template_name = 'type_transport/main.html'

    def post(self, request, *args, **kwargs):
        context2 = {
            'erros': []
        }
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        data = request.POST
        print("#########################")
        print(data)
        form = TTF(data)
        if form.is_valid():
            form.write(request.user.id)
            response['msj'] = "Se ha actualizado '{}' correctamente".format(data['name'])
        else:
            response['msj'] = "Ha ocurrido un error al querer Guardar el dato '{}'".format(data['name'])
        context2['response'] = response
        return render(
            request,
            'type_transport/main.html',
            context2,
        )

class DatatablesActiveToggleRules(LoginRequiredMixin, TemplateView):
    template_name = 'typetransport/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        print("*********************")
        id = int(request.POST['id'])
        print(id)
        actionx = int(request.POST['action'])
        print(actionx)
        tt = T.objects.get(pk=id)
        print(tt)
        if actionx == 0:
            tt.active = False
            print("**")
            print(tt)
            tt.save()
            response[
                "msj"] = 'Se ha archivado el tipo de transporte. No podrá ser utilizado en las condiciones.'
        else:
            tt.active = True
            tt.save()
            response[
                "msj"] = 'Se ha desarchivado el tipo de transporte. Ya puedes utilizar el modelo en las condiciones.'
        print("*********************")
        return JsonResponse(response)


class DatatablesDeleteRules(LoginRequiredMixin, TemplateView):
    template_name = 'type_transport/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        print("*********************")
        id = int(request.POST['id'])
        tt = T.objects.get(pk=id)
        if tt.delete():
            response['msj'] = "Se ha eliminado el tipo de transporte correctamente."
        else:
            response['msj'] = "Hubo un error cuando se in intento borrar el tipo de transporte."
            response['error'] = True
        print("*********************")
        return JsonResponse(response)

@login_required
def ShowId(request):
    id = request.GET['id']
    csrfmiddlewaretoken = request.GET['csrfmiddlewaretoken']
    print("******************************************************* >>>")
    print(id)
    tt = T.objects.filter(id=id).all().values()[0]
    data = {
        'id': id,
        'name' : tt["name"],
        'volumen' : tt["volumen"],
        'capacity_pallet' : tt["capacity_pallet"],
    }
    print(data)
    form = TTF(data)
    form.erros = []
    context = {
        "csrfmiddlewaretoken":csrfmiddlewaretoken,
        "form":form,
        "id": id,
        "name": data["name"],
        "first":True
    }
    print(context)
    print("******************************************************* <<<")
    return render(
        request=request,
        template_name='type_transport/show.html',
        context=context
    )
