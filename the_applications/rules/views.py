#django
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from the_applications.rules.forms import ModelsRule as MR, ModelsRuleUpdate as MR2, HeaderRule as HM
from the_applications.datasheet.models import ModelReg as MoReg, Header as Cond
from the_applications.rules.models import Model as M
from django.apps import apps
from django.contrib.auth.decorators import login_required
import psycopg2
import requests
import the_applications.func as f
from django.contrib.auth.models import User
from the_applications.notify.models import TypeNotify, Notify
from django.shortcuts import render, redirect

from the_applications.notify.forms import NotifyForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
import json
import the_applications.func as f
from datetime import datetime, timezone
import timeago
# Model

class Principal(LoginRequiredMixin, TemplateView):
    template_name = 'rules/main.html'

    def get_context_data(self, **kwargs):
        context2 = super().get_context_data(**kwargs)
        fmodel = MR()
        fheader = HM()
        context2["models"] = fmodel
        context2["header"] = fheader
        return context2


class Modelx2(LoginRequiredMixin, TemplateView):
    template_name = 'rules/main.html'

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
        file = request.FILES
        print("---------------------------------->")
        print(data)
        print(file)
        print("---------------------------------->")


class Modelx(LoginRequiredMixin, TemplateView):
    template_name = 'rules/main.html'

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
        file = request.FILES
        form = MR(data,file)
        if form.is_valid():
            type = data["type"]
            print("********************** [START EVAL]")
            print(type)
            if type == "internal":
                fields = data["tinternal_fields"]
                tinternal_code = data["tinternal_code"]
                tinternal_model = data["tinternal_model"]
                if not len(tinternal_code) > 0 :
                    response["msj"] = """{} ▪ No existe el nombre de la tabla.""".format(response["msj"])
                    response["error"] = True
                if not len(tinternal_model) > 0 :
                    response["msj"] = """{} ▪ No existe el nombre del modelo django.""".format(response["msj"])
                    response["error"] = True
                if not len(fields) > 0 :
                    response["msj"] = """{} ▪ No existen campos del modelo.""".format(response["msj"])
                    response["error"] = True
                if response["error"]:
                    response["msj"] = """{} ▪ "Los datos son necesarios". """.format(response["msj"])
                else:
                    response["msj"] = "Se ha guardado el modelo y ya puede ser utilizado en las condiciones."
                    if tinternal_code == "current":
                        tinternal_code = 'datasheet_datasheet'
                    model = next((m for m in apps.get_models() if m._meta.db_table==tinternal_code), None)
                    if model:
                        model2 = MoReg.objects.filter(name=tinternal_model).all()
                        if model2:
                            print("**************************")
                            print("---> ", model2)
                            form.save(user=request.user.id)
                            type_notify = TypeNotify.objects.get(pk=1)
                            new_notify = Notify(
                                user=request.user,
                                type=type_notify,
                                name="Nuevo modelo Interno - {}".format(str(tinternal_model)),
                                description="""
                                                   El usuario "{} {}"  ha generado un nuevo modelo de tipo "INTERNO" con
                                                    el identificador "{}". Este tipo de modelos interactuan directamente
                                                    con la base de Datos de Roadly, Ocupando cualquier catalogo interno
                                                    como herramienta de evalución.
                                                    
                                                    
                                                   """.format(request.user.first_name, request.user.last_name,
                                                              str(tinternal_model)),
                                priority=1,
                                picture='notify/pictures/model.png'
                            )
                            new_notify.save()
                        else:
                            response["msj"] = """No coincide el nombre de modelo de DJango con alguno existente en Roadly"""
                            response["error"] = True
                    else:
                        response["msj"] = """No coincide el nombre de la tabla con algun existente en Roadly"""
                        response["error"] = True
                    print("***********************")
            elif type == "external":
                print("*********************** [External Start]")
                texternal_host = data["texternal_host"]
                texternal_user = data["texternal_user"]
                texternal_password = data["texternal_password"]
                texternal_port = data["texternal_port"]
                texternal_db = data["texternal_db"]
                texternal_query = data["texternal_query"]
                texternal_code = data["texternal_code"]
                texternal_model = data["texternal_model"]
                texternal_fields = data["texternal_fields"]
                if not len(texternal_host) > 0 :
                    response["msj"] = """{} ▪ No existe el Host de conexión a DB.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_user) > 0 :
                    response["msj"] = """{} ▪ No existe el Usuario de conexión a DB.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_password) > 0 :
                    response["msj"] = """{} ▪ No existe la Contraseña de conexión a DB.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_port) > 0 :
                    response["msj"] = """{} ▪ No existe el Puerto de conexión a DB.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_db) > 0 :
                    response["msj"] = """{} ▪ No existe el Nombre de la DB.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_query) > 0 :
                    response["msj"] = """{} ▪ No existe Query para la extracción de información.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_code) > 0 :
                    response["msj"] = """{} ▪ No existe el Nombre técnico de la extracción.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_model) > 0 :
                    response["msj"] = """{} ▪ No existe el Nombre de la Tablas o Vista.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_fields) > 0 :
                    response["msj"] = """{} ▪ No hay campos que extraer. Es importante colocar los campos a utilizar.""".format(response["msj"])
                    response["error"] = True
                if response["error"]:
                    response["msj"] = """{} ▪ "Los datos son necesarios". """.format(response["msj"])
                else:
                    params = {
                        "host": texternal_host,
                        "port": texternal_port,
                        "user": texternal_user,
                        "password": texternal_password,
                        "database": texternal_db
                    }
                    conn = psycopg2.connect(**params)
                    if conn:
                        cur = conn.cursor()
                        cur.execute(texternal_query)
                        xquery = cur.fetchall()
                        if len(xquery) > 0:
                            print("************************** [Se guarda modelo - START] ")
                            response["error"] = False
                            response["msj"] = "Se ha guardado el modelo y ya puede ser utilizado en las condiciones."
                            form.save(user=request.user.id)
                            type_notify = TypeNotify.objects.get(pk=1)
                            new_notify = Notify(
                                user=request.user,
                                type=type_notify,
                                name="Nuevo modelo Postgresql - {}".format(str(texternal_model)),
                                description="""
                                           El usuario "{} {}"  ha generado un nuevo modelo de tipo "EXTERNO" con
                                            el identificador "{}". Este tipo de modelos generan una relación ODBC           
                                            con alguna base de datos generada Postgresql. Dentro de los parámetros
                                            de alta, existe un campo Query de evalución de la consulta. 
                                            Tenemos que tener cuidado que previamente este modelo se evalue en un 
                                            ambiente controlado de pruebas fuera de Roadly para garantizar que los 
                                            campos contenidos son los que la consulta arroja. Recordar que los campos 
                                            a evaluar serán tal cual se especifiquen en el Query. Se sugiere ocupar ALIAS.  
                                           """.format(request.user.first_name,
                                                      request.user.last_name,
                                                      str(texternal_model)),
                                priority=1,
                                picture='notify/pictures/model.png'
                            )
                            new_notify.save()
                            print("************************** [Se guarda modelo - START] ")
                        else:
                            response["msj"] = """La evaluación del Query fallo. Revisa la sentencia de extracción.""";
                            response["error"] = True
                    else:
                        response["msj"] = """No fue posible establecer una conexión con la base de datos Posgresql con los parametros ingresados. Favor de revisar la información.""";
                        response["error"] = True
                print("*********************** [External End]")
            elif type == "file":
                print("*********************** [File Start]")
                tfile_code = data["tfile_code"]
                tfile_fields = data["tfile_fields"]
                if not len(tfile_code) > 0 :
                    response["msj"] = """{} ▪ Es necesario ingresar el nombre del archivo completo con extensión.""".format(response["msj"])
                    response["error"] = True
                if not len(tfile_fields) > 0 :
                    response["msj"] = """{} ▪ No hay campos para la evaluación.""".format(response["msj"])
                    response["error"] = True
                if response["error"]:
                    response["msj"] = """{} ▪ "Los datos son necesarios". """.format(response["msj"])
                else:
                    if file["file"]:
                        response["error"] = False
                        response["msj"] = "Se ha guardado el modelo y ya puede ser utilizado en las condiciones."
                        form.save(user=request.user.id)
                        type_notify = TypeNotify.objects.get(pk=1)
                        new_notify = Notify(
                            user=request.user,
                            type=type_notify,
                            name="Nuevo modelo CSV - {}".format(str(tfile_code)),
                            description="""
                                       El usuario "{} {}"  ha generado un nuevo modelo de tipo "FILE" con
                                        el identificador "{}". Este tipo de modelos generan una relación con un archivo
                                        texto plano en formato CSV. Todos los modelos de este tipo requiren que el 
                                        contenido tenga como primer linea la cabecera de la información que posteriormente
                                        será asociada con los campos a evaluar.  
                                       """.format(request.user.first_name,
                                                  request.user.last_name,
                                                  str(tfile_code)),
                            priority=1,
                            picture='notify/pictures/model.png'
                        )
                        new_notify.save()
                    else:
                        response["msj"] = """▪ No archivos para ser cargados en la solicitud."""
                        response["error"] = True
                print("*********************** [File End]")
            elif type == "api":
                print("*********************** [EndPoint Start]")
                tapi_code = data["tapi_code"]
                tapi_endpoint = data["tapi_endpoint"]
                tapi_fields = data["tapi_fields"]
                tapi_structure = data["tapi_structure"]
                if not len(tapi_code) > 0:
                    response["msj"] = """{} ▪ Es necesario ingresar el nombnre del EndPoint""".format(response["msj"])
                    response["error"] = True
                if not len(tapi_endpoint) > 0:
                    response["msj"] = """{} ▪ Ingresar la URL del EnPoint.""".format(response["msj"])
                    response["error"] = True
                if not len(tapi_fields) > 0:
                    response["msj"] = """{} ▪ No hay campos para la evaluación.""".format(response["msj"])
                    response["error"] = True
                if not len(tapi_structure) > 0:
                    response["msj"] = """{} ▪ No hay estructura necesaria para la evalución.""".format(response["msj"])
                    response["error"] = True
                if response["error"]:
                    response["msj"] = """{} ▪ "Los datos son necesarios". """.format(response["msj"])
                else:
                    response2 = requests.get(tapi_endpoint, params={})
                    print(response2)
                    if response2.status_code == 200:
                        response["error"] = False
                        response["msj"] = "Se ha guardado el modelo y ya puede ser utilizado en las condiciones."
                        form.save(user=request.user.id)
                        type_notify = TypeNotify.objects.get(pk=1)
                        new_notify = Notify(
                            user=request.user,
                            type=type_notify,
                            name="Nuevo modelo API - {}".format(str(tapi_code)),
                            description="""
                                           El usuario "{} {}"  ha generado un nuevo modelo de tipo "API" con
                                            el identificador "{}". Este tipo de modelos generan una relación con una API
                                            para consumo. Esta URL permite extraer la información de una manera externa
                                            a partir de una estructura de datos previamente cargada en el formulario.  
                                           """.format(request.user.first_name,
                                                      request.user.last_name,
                                                      str(tapi_code)),
                            priority=1,
                            picture='notify/pictures/model.png'
                        )
                        new_notify.save()
                    else:
                        response["msj"] = """▪ No archivos para ser cargados en la solicitud."""
                        response["error"] = True
                print("*********************** [EndPoint End]")
        else:
            print(str(form.errors))
            if "El nombre del modelo ya ha sido registrado" in str(form.errors):
                err = "El nombre del modelo ya ha sido registrado."
            else:
                err = ""
            response["msj"] = err
            response["error"] = True
        context2['models'] = form
        context2['user'] = request.user
        context2['response'] = response
        return render(
            request,
            'rules/main.html',
            context2,
        )
class UpdateModel(LoginRequiredMixin, TemplateView):
    template_name = 'rules/main.html'

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
        form = MR2(data)
        if form.is_valid():
            type = data["type"]
            print("********************** [START EVAL]")
            print(type)
            if type == "internal":
                fields = data["tinternal_fields"]
                tinternal_code = data["tinternal_code"]
                tinternal_model = data["tinternal_model"]
                if not len(tinternal_code) > 0 :
                    response["msj"] = """{} ▪ No existe el nombre de la tabla.""".format(response["msj"])
                    response["error"] = True
                if not len(tinternal_model) > 0 :
                    response["msj"] = """{} ▪ No existe el nombre del modelo django.""".format(response["msj"])
                    response["error"] = True
                if not len(fields) > 0 :
                    response["msj"] = """{} ▪ No existen campos del modelo.""".format(response["msj"])
                    response["error"] = True
                if response["error"]:
                    response["msj"] = """{} ▪ "Los datos son necesarios". """.format(response["msj"])
                else:
                    response["msj"] = "Se ha guardado el modelo y ya puede ser utilizado en las condiciones."
                    if tinternal_code == "current":
                        tinternal_code = 'datasheet_datasheet'
                    model = next((m for m in apps.get_models() if m._meta.db_table==tinternal_code), None)
                    if model:
                        model2 = MoReg.objects.filter(name=tinternal_model).all()
                        if model2:
                            print("**************************")
                            print("---> ", model2)
                            form.write(user=request.user.id)
                            type_notify = TypeNotify.objects.get(pk=1)
                            new_notify = Notify(
                                user=request.user,
                                type=type_notify,
                                name="Actualización modelo - {}".format(str(tinternal_model)),
                                description="""
                                           El usuario "{} {}"  ha actualizado el modelo de tipo "INTERNO" con
                                            el identificador "{}". 
                                           """.format(request.user.first_name,
                                                      request.user.last_name,
                                                      str(tinternal_model)),
                                priority=1,
                                picture='notify/pictures/update.png'
                            )
                            new_notify.save()
                        else:
                            response["msj"] = """No coincide el nombre de modelo de DJango con alguno existente en Roadly"""
                            response["error"] = True
                    else:
                        response["msj"] = """No coincide el nombre de la tabla con algun existente en Roadly"""
                        response["error"] = True
                    print("***********************")
            elif type == "external":
                print("*********************** [External Start]")
                texternal_host = data["texternal_host"]
                texternal_user = data["texternal_user"]
                texternal_password = data["texternal_password"]
                texternal_port = data["texternal_port"]
                texternal_db = data["texternal_db"]
                texternal_query = data["texternal_query"]
                texternal_code = data["texternal_code"]
                texternal_model = data["texternal_model"]
                texternal_fields = data["texternal_fields"]
                if not len(texternal_host) > 0 :
                    response["msj"] = """{} ▪ No existe el Host de conexión a DB.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_user) > 0 :
                    response["msj"] = """{} ▪ No existe el Usuario de conexión a DB.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_password) > 0 :
                    response["msj"] = """{} ▪ No existe la Contraseña de conexión a DB.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_port) > 0 :
                    response["msj"] = """{} ▪ No existe el Puerto de conexión a DB.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_db) > 0 :
                    response["msj"] = """{} ▪ No existe el Nombre de la DB.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_query) > 0 :
                    response["msj"] = """{} ▪ No existe Query para la extracción de información.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_code) > 0 :
                    response["msj"] = """{} ▪ No existe el Nombre técnico de la extracción.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_model) > 0 :
                    response["msj"] = """{} ▪ No existe el Nombre de la Tablas o Vista.""".format(response["msj"])
                    response["error"] = True
                if not len(texternal_fields) > 0 :
                    response["msj"] = """{} ▪ No hay campos que extraer. Es importante colocar los campos a utilizar.""".format(response["msj"])
                    response["error"] = True
                if response["error"]:
                    response["msj"] = """{} ▪ "Los datos son necesarios". """.format(response["msj"])
                else:
                    params = {
                        "host": texternal_host,
                        "port": texternal_port,
                        "user": texternal_user,
                        "password": texternal_password,
                        "database": texternal_db
                    }
                    conn = psycopg2.connect(**params)
                    if conn:
                        cur = conn.cursor()
                        cur.execute(texternal_query)
                        xquery = cur.fetchall()
                        if len(xquery) > 0:
                            print("************************** [Se actualiza modelo - START] ")
                            response["error"] = False
                            response["msj"] = "Se ha guardado el modelo y ya puede ser utilizado en las condiciones."
                            form.write(user=request.user.id)
                            type_notify = TypeNotify.objects.get(pk=1)
                            new_notify = Notify(
                                user=request.user,
                                type=type_notify,
                                name="Actualización modelo - {}".format(str(texternal_model)),
                                description="""
                                               El usuario "{} {}"  ha actualizado el modelo de tipo "EXTERNO" con
                                                el identificador "{}". 
                                               """.format(request.user.first_name,
                                                          request.user.last_name,
                                                          str(texternal_model)),
                                priority=1,
                                picture='notify/pictures/update.png'
                            )
                            new_notify.save()
                            print("************************** [Se actualiza modelo - START] ")
                        else:
                            response["msj"] = """La evaluación del Query fallo. Revisa la sentencia de extracción.""";
                            response["error"] = True
                    else:
                        response["msj"] = """No fue posible establecer una conexión con la base de datos Posgresql con los parametros ingresados. Favor de revisar la información.""";
                        response["error"] = True
                print("*********************** [External End]")
            elif type == "file":
                print("*********************** [File Start]")
                tfile_code = data["tfile_code"]
                tfile_fields = data["tfile_fields"]
                if not len(tfile_code) > 0 :
                    response["msj"] = """{} ▪ Es necesario ingresar el nombre del archivo completo con extensión.""".format(response["msj"])
                    response["error"] = True
                if not len(tfile_fields) > 0 :
                    response["msj"] = """{} ▪ No hay campos para la evaluación.""".format(response["msj"])
                    response["error"] = True
                if response["error"]:
                    response["msj"] = """{} ▪ "Los datos son necesarios". """.format(response["msj"])
                else:
                    if data["file"]:
                        response["error"] = False
                        response["msj"] = "Se ha guardado el modelo y ya puede ser utilizado en las condiciones."
                        form.write(user=request.user.id)
                        type_notify = TypeNotify.objects.get(pk=1)
                        new_notify = Notify(
                            user=request.user,
                            type=type_notify,
                            name="Actualización modelo - {}".format(str(tfile_code)),
                            description="""
                                       El usuario "{} {}"  ha actualizado el modelo de tipo "FILE" con
                                        el identificador "{}". 
                                       """.format(request.user.first_name,
                                                  request.user.last_name,
                                                  str(tfile_code)),
                            priority=1,
                            picture='notify/pictures/update.png'
                        )
                        new_notify.save()
                    else:
                        response["msj"] = """▪ No archivos para ser cargados en la solicitud."""
                        response["error"] = True
                print("*********************** [File End]")
            elif type == "api":
                print("*********************** [EndPoint Start]")
                tapi_code = data["tapi_code"]
                tapi_endpoint = data["tapi_endpoint"]
                tapi_fields = data["tapi_fields"]
                tapi_structure = data["tapi_structure"]
                if not len(tapi_code) > 0:
                    response["msj"] = """{} ▪ Es necesario ingresar el nombnre del EndPoint""".format(response["msj"])
                    response["error"] = True
                if not len(tapi_endpoint) > 0:
                    response["msj"] = """{} ▪ Ingresar la URL del EnPoint.""".format(response["msj"])
                    response["error"] = True
                if not len(tapi_fields) > 0:
                    response["msj"] = """{} ▪ No hay campos para la evaluación.""".format(response["msj"])
                    response["error"] = True
                if not len(tapi_structure) > 0:
                    response["msj"] = """{} ▪ No hay estructura necesaria para la evalución.""".format(response["msj"])
                    response["error"] = True
                if response["error"]:
                    response["msj"] = """{} ▪ "Los datos son necesarios". """.format(response["msj"])
                else:
                    response2 = requests.get(tapi_endpoint, params={})
                    print(response2)
                    if response2.status_code == 200:
                        response["error"] = False
                        response["msj"] = "Se ha guardado el modelo y ya puede ser utilizado en las condiciones."
                        form.write(user=request.user.id)
                        type_notify = TypeNotify.objects.get(pk=1)
                        new_notify = Notify(
                            user=request.user,
                            type=type_notify,
                            name="Actualización modelo - {}".format(str(tapi_code)),
                            description="""
                                       El usuario "{} {}"  ha actualizado el modelo de tipo "FILE" con
                                        el identificador "{}". 
                                       """.format(request.user.first_name,
                                                  request.user.last_name,
                                                  str(tapi_code)),
                            priority=1,
                            picture='notify/pictures/update.png'
                        )
                        new_notify.save()
                    else:
                        response["msj"] = """▪ No archivos para ser cargados en la solicitud."""
                        response["error"] = True
                print("*********************** [EndPoint End]")
        else:
            print(str(form.errors))
            if "El nombre del modelo ya ha sido registrado" in str(form.errors):
                err = "El nombre del modelo ya ha sido registrado."
            else:
                err = ""
            response["msj"] = err
            response["error"] = True

        context2['models'] = form
        context2['user'] = request.user
        context2['response'] = response
        return render(
            request,
            'rules/main.html',
            context2,
        )

class DatatablesModel(LoginRequiredMixin, TemplateView):
    template_name = 'rules/main.html'


    def post(self, request, *args, **kwargs):

        query = M.objects.all().values(
            'id',
            'name',
            'tinternal_code',
            'tinternal_model',
            'texternal_code',
            'texternal_model',
            'tfile_code',
            'tapi_code',
            'type',
            'delete',
            'status',
            'active'
        )
        response = {
            'data':[],
            'error': False,
            'msj':''
        }
        data = []
        for q in query:
            if "internal" ==  q['type']:
                item = {
                    'id':q["id"],
                    'name':q["name"],
                    'code':q["tinternal_code"],
                    'model':q["tinternal_model"],
                    'type': next((x[1] for x in M.TYPE if x[0] == q["type"]), ""),
                    'xdelete': q["delete"],
                    'status': next((x[1] for x in M.STATUS if x[0] == q['status']), ""),
                    'active': q["active"]
                }
                data.append(item)
            elif "external" ==  q['type']:
                item = {
                    'id':q["id"],
                    'name':q["name"],
                    'code':q["texternal_code"],
                    'model':q["texternal_model"],
                    'type': next((x[1] for x in M.TYPE if x[0] == q["type"]), ""),
                    'xdelete': q["delete"],
                    'status': next((x[1] for x in M.STATUS if x[0] == q['status']), ""),
                    'active': q["active"]
                }
                data.append(item)
            elif "file" ==  q['type']:
                item = {
                    'id':q["id"],
                    'name':q["name"],
                    'code':q["tfile_code"],
                    'model':"",
                    'type': next((x[1] for x in M.TYPE if x[0] == q["type"]), ""),
                    'xdelete': q["delete"],
                    'status': next((x[1] for x in M.STATUS if x[0] == q['status']), ""),
                    'active': q["active"]
                }
                data.append(item)
            elif "api" ==  q['type']:
                item = {
                    'id':q["id"],
                    'name':q["name"],
                    'code':q["tapi_code"],
                    'model':"",
                    'type': next((x[1] for x in M.TYPE if x[0] == q["type"]), ""),
                    'xdelete': q["delete"],
                    'status': next((x[1] for x in M.STATUS if x[0] == q['status']), ""),
                    'active': q["active"]
                }
                data.append(item)
        response['data']=data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2

class DatatablesDeleteRules(LoginRequiredMixin, TemplateView):
    template_name = 'rules/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        print("*********************")
        id = int(request.POST['id'])
        rule = M.objects.filter(id=id).all()
        status = rule[0].status
        if status == "ready":
            if rule.delete():
                response['msj'] = "Se ha eliminado el modelo correctamente."
            else:
                response['msj'] = "Hubo un error cuando se in intento borrar el modelo."
                response['error'] = True
        print("*********************")
        return JsonResponse(response)

class DatatablesActiveToggleRules(LoginRequiredMixin, TemplateView):
    template_name = 'rules/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        print("*********************")
        id = int(request.POST['id'])
        actionx = int(request.POST['action'])
        rule = M.objects.filter(id=id).all()
        status = rule[0].status
        name = rule[0].name
        rl = rule[0]
        if status == "ready":
            if actionx == 0:
                action = False
            else:
                action = True
            if action == False:
                rl.active = False
                rl.save()
                response["msj"] = 'Se ha archivado el Modelo "<b>{}</b>". No podrá ser utilizado en las condiciones.'.format(name)
            else:
                rl.active = True
                rl.save()
                response["msj"] = 'Se ha desarchivado el Modelo "<b>{}</b>". Ya puedes utilizar el modelo en las condiciones.'.format(name)
        print("*********************")
        return JsonResponse(response)

@login_required
def ShowId(request):
    id = request.GET['id']
    csrfmiddlewaretoken = request.GET['csrfmiddlewaretoken']
    print("******************************************************* >>>")
    rule = M.objects.filter(id=id).all()[0]
    print(rule)
    data = {
        'id': id,
        'name' : rule.name,
        'description' : rule.description,
        'type' : rule.type,
        'tinternal_code' : rule.tinternal_code,
        'tinternal_model' : rule.tinternal_model,
        'tinternal_fields' : rule.tinternal_fields,
        'texternal_host' : rule.texternal_host,
        'texternal_user' : rule.texternal_user,
        'texternal_password' : rule.texternal_password,
        'texternal_port' : rule.texternal_port,
        'texternal_db' : rule.texternal_db,
        'texternal_query' : rule.texternal_query,
        'texternal_code' : rule.texternal_code,
        'texternal_model' : rule.texternal_model,
        'texternal_fields' : rule.texternal_fields,
        'tfile_code' : rule.tfile_code,
        'tfile_path' : rule.tfile_path,
        'file' : rule.tfile_binary,
        'tfile_fields' : rule.tfile_fields,
        'tapi_code' : rule.tapi_code,
        'tapi_endpoint' : rule.tapi_endpoint,
        'tapi_fields' : rule.tapi_fields,
        'tapi_structure' : rule.tapi_structure
    }
    form = MR2(data)
    print(rule.name)
    context = {
        "csrfmiddlewaretoken":csrfmiddlewaretoken,
        "models":form,
        "name": rule.name,
        "type": rule.type,
        "id": id
    }
    print(context)
    print("******************************************************* <<<")
    return render(
        request=request,
        template_name='rules/show.html',
        context=context
    )

class PostGetFieldsModelId(LoginRequiredMixin, TemplateView):
    template_name = 'rules/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = int(request.POST['idx'])
        print(id)
        datos = M.objects.filter(id=id).all().values()[0]
        dtype = datos['type']
        dfield = []
        if dtype == "internal":
            dfield = datos["tinternal_fields"]
        if dtype == "external":
            dfield = datos["texternal_fields"]
        if dtype == "file":
            dfield = datos["tfile_fields"]
        if dtype == "api":
            dfield = datos["tapi_fields"]
        print(dfield)
        response['data'] = dfield
        return JsonResponse(response)