#django
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from the_applications.zones.forms import ModelForms as MF, EdosForms as ME, ModelForms2 as MFU
from the_applications.zones.models import Model as M, Edos as E
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from the_applications.notify.models import TypeNotify, Notify
from django.contrib.auth.decorators import login_required
# Model

class Principal(LoginRequiredMixin, TemplateView):
    template_name = 'zones/main.html'

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
        print("************************************ >")
        print(data)
        print("************************************ <")
        form = MF(data)
        if form.is_valid():
            name = data["name"]
            form.save(user=request.user.id)
            type_notify = TypeNotify.objects.get(pk=1)
            new_notify = Notify(
                user=request.user,
                type=type_notify,
                name="Nuevo Estado - {}".format(str(name)),
                description="""
                                                       El usuario "{} {}"  ha generado un nuevo Estado 
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
            'zones/main.html',
            context,
        )

    def get_context_data(self, **kwargs):
        context2 = super().get_context_data(**kwargs)
        form1 = MF()
        form2 = ME()
        context2['form1'] = form1
        context2['form2'] = form2
        context2['name_model'] = "Zonas"
        context2['name_model2'] = "Estados"
        return context2

class Estados(LoginRequiredMixin, TemplateView):
    template_name = 'zones/main.html'

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
        form = ME(data)
        if form.is_valid():
            name = data["name"]
            form.save(user=request.user.id)

            type_notify = TypeNotify.objects.get(pk=1)
            new_notify = Notify(
                user=request.user,
                type=type_notify,
                name="Nuevo Estado - {}".format(str(name)),
                description="""
                                                       El usuario "{} {}"  ha generado un nuevo estado
                                                        con nombre "{}". Ya puede ser utilizado para los modelos
                                                        de evaluación del sitema dentro de las condiciones.
                                                       """.format(request.user.first_name,
                                                                  request.user.last_name,
                                                                  str(name)),
                priority=1,
                picture='notify/pictures/edos.png'
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
            'zones/main.html',
            context,
        )

class PostGetStates(LoginRequiredMixin, TemplateView):
    template_name = 'zones/main.html'


    def post(self, request, *args, **kwargs):

        query = E.objects.all().values()
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
                'active': q["active"],
            }
            data.append(item)
        response['data']=data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2


class DataTablesInfoEdos(LoginRequiredMixin, TemplateView):
    template_name = 'zones/main.html'


    def post(self, request, *args, **kwargs):

        query = E.objects.all().values()
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
                'active': q["active"],
            }
            data.append(item)
        response['data']=data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2

class DataTablesInfoModel(LoginRequiredMixin, TemplateView):
    template_name = 'zones/main.html'


    def post(self, request, *args, **kwargs):

        query = M.objects.all().values()
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
                'description': q["description"],
                'edos': q["edos"],
                'code': q["code"],
                'number_code': q["number_code"],
                'active': q["active"],
            }
            data.append(item)
        response['data']=data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2


class UpdateModelEdos(LoginRequiredMixin, TemplateView):
    template_name = 'zones/main.html'

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
        form = ME(data)
        if form.is_valid():
            name = data["name"]
            form.write(request.user.id)
            type_notify = TypeNotify.objects.get(pk=1)
            new_notify = Notify(
                user=request.user,
                type=type_notify,
                name="Actualización de Estado - {}".format(str(name)),
                description="""
                           El usuario "{} {}"  ha actualizado el estado
                            con nombre "{}". Ya puede ser utilizado para los modelos
                            de evaluación del sitema dentro de las condiciones.
                           """.format(request.user.first_name,
                                      request.user.last_name,
                                      str(name)),
                priority=1,
                picture='notify/pictures/edos.png'
            )
            new_notify.save()
            response['msj'] = "Se ha actualizado '{}' correctamente".format(data['name'])
        else:
            response['msj'] = "Ha ocurrido un error al querer Guardar el dato '{}'".format(data['name'])
        context2['response'] = response
        return render(
            request,
            'zones/main.html',
            context2,
        )
class UpdateModelModel(LoginRequiredMixin, TemplateView):
    template_name = 'zones/main.html'

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
        print("######################### :v")
        print(data)
        form = MFU(data)
        print("~~~~~~~~~~~")
        print(form)
        print("~~~~~~~~~~~")
        if form.is_valid():
            print("~~~~~~~~~~~ ****")
            name = data["name"]
            print("~~~~~~~~~~~ ****")
            form.write(request.user.id)
            type_notify = TypeNotify.objects.get(pk=1)
            new_notify = Notify(
                user=request.user,
                type=type_notify,
                name="Actualización de Zona - {}".format(str(name)),
                description="""
                                       El usuario "{} {}"  ha actualizado la zona
                                        con nombre "{}". Ya puede ser utilizado para los modelos
                                        de evaluación del sitema dentro de las condiciones.
                                       """.format(request.user.first_name,
                                                  request.user.last_name,
                                                  str(name)),
                priority=1,
                picture='notify/pictures/zone.png'
            )
            new_notify.save()
            response['msj'] = "Se ha actualizado '{}' correctamente".format(data['name'])
        else:
            response['error'] = True
            response['msj'] = "Ha ocurrido un error al querer Guardar el dato '{}-{}'".format(data['name'],form.errors)
        context2['response'] = response
        return render(
            request,
            'zones/main.html',
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

class DatatablesActiveToggleRulesEdos(LoginRequiredMixin, TemplateView):
    template_name = 'zones/main.html'

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
        tt = E.objects.get(pk=id)
        print(tt)
        if actionx == 0:
            tt.active = False
            print("**")
            print(tt)
            tt.save()
            response[
                "msj"] = 'Se ha archivado el Estado. No podrá ser utilizado en las condiciones.'
        else:
            tt.active = True
            tt.save()
            response[
                "msj"] = 'Se ha desarchivado el Estado. Ya puedes utilizar el modelo en las condiciones.'
        print("*********************")
        return JsonResponse(response)

class DatatablesActiveToggleRulesModel(LoginRequiredMixin, TemplateView):
    template_name = 'zones/main.html'

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
        tt = M.objects.get(pk=id)
        print(tt)
        if actionx == 0:
            tt.active = False
            print("**")
            print(tt)
            tt.save()
            response[
                "msj"] = 'Se ha archivado el Estado. No podrá ser utilizado en las condiciones.'
        else:
            tt.active = True
            tt.save()
            response[
                "msj"] = 'Se ha desarchivado el Estado. Ya puedes utilizar el modelo en las condiciones.'
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

class DatatablesDeleteRulesEdos(LoginRequiredMixin, TemplateView):
    template_name = 'zones/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        print("*********************")
        id = int(request.POST['id'])
        tt = E.objects.get(pk=id)
        if tt.delete():
            response['msj'] = "Se ha eliminado el Estado correctamente."
        else:
            response['msj'] = "Hubo un error cuando se in intento borrar el Estado."
            response['error'] = True
        print("*********************")
        return JsonResponse(response)

class DatatablesDeleteRulesModel(LoginRequiredMixin, TemplateView):
    template_name = 'zones/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        print("*********************")
        id = int(request.POST['id'])
        tt = M.objects.get(pk=id)
        if tt.delete():
            response['msj'] = "Se ha eliminado la Zona correctamente."
        else:
            response['msj'] = "Hubo un error cuando se in intento borrar la Zona."
            response['error'] = True
        print(response)
        print("*********************")
        return JsonResponse(response)

@login_required
def ShowIdEdos(request):
    id = request.GET['id']
    csrfmiddlewaretoken = request.GET['csrfmiddlewaretoken']
    print("******************************************************* >>>")
    print(id)
    tt = E.objects.filter(id=id).all().values()[0]
    data = {
        'id': id,
        'name' : tt["name"]
    }
    print(data)
    form = ME(data)
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
        template_name='zones/showedos.html',
        context=context
    )

@login_required
def ShowIdModel(request):
    id = request.GET['id']
    csrfmiddlewaretoken = request.GET['csrfmiddlewaretoken']
    print("******************************************************* >>>")
    print(id)
    tt = M.objects.filter(id=id).all().values()[0]
    data = {
        'id': id,
        'name' : tt["name"],
        'description' : tt["description"],
        'edos' : tt["edos"],
        'code' : tt["code"],
        'number_code' : tt["number_code"]
    }
    print(data)
    form = MF(data)
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
        template_name='zones/showmodel.html',
        context=context
    )
