"""Apps forms."""
import os
# Django
from django import forms
from the_applications.notify.models import TypeNotify, Notify
from django.contrib.auth.models import User
from django.db.models import Q
from the_applications.rules.models import Model as Modru, Header as Cond
from the_applications.conexion import selecciona_basedatos
import datetime as dt


class ModelsRule(forms.Form):

    TYPE = Modru.TYPE

    type = forms.ChoiceField(
        label="Tipo de modelo",
        choices=TYPE,
        widget=forms.Select(attrs={'class': 'form-control rc-main', 'required': True})
    )
    name = forms.CharField(
        label="Nombre de Modelo",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-main', 'required': True}),
        help_text="Nombre legible para el usuario final"
    )
    description = forms.CharField(
        label="Descripción de Modelo",
        help_text="Describe la procedencia y el contexto del modelo.",
        widget=forms.Textarea(attrs={'class': 'form-control rc-main', 'required': True, "rows":"5"})
    )
    tinternal_code = forms.CharField(
        label="Nombre de tabla",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-internal rc-initial'}),
        help_text="Nombre de la tabla de la datos registrada en Roadly"
    )
    tinternal_model = forms.CharField(
        label="Nombre del modelo DJango",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-internal'}),
        help_text="Nombre del modelo de DJango registrado"
    )
    tinternal_fields = forms.CharField(
        label="Campos del modelo",
        help_text="Se agregan los campos que pueden ser seleccionados del modelo.",
        widget=forms.Textarea(attrs={'class': 'form-control rc-internal rc-internal--field', 'readonly': True, "rows": "5"})
    )
    texternal_host = forms.CharField(
        label="Host DB",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="DNS o IP de conexión a la base de datos de Postgres"
    )
    texternal_user = forms.CharField(
        label="Usuario DB",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="Usuario de la base de datos Postgres"
    )
    texternal_password = forms.CharField(
        label="Password DB",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="Password de la base de datos Postgres"
    )
    texternal_port = forms.CharField(
        label="Port DB",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="Puerto de la base de datos Postgres"
    )
    texternal_db = forms.CharField(
        label="Nombre DB",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="Nombre de la base de datos Postgres"
    )
    texternal_query = forms.CharField(
        label="Query de extracción",
        help_text="Se el Query de la extracción de base datos.",
        widget=forms.Textarea(
            attrs={'class': 'form-control rc-external', "rows": "5"})
    )
    texternal_code = forms.CharField(
        label="Nombre de tabla",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="Nombre de la tabla de la datos externa."
    )
    texternal_model = forms.CharField(
        label="Nombre de la Entidad o Vista",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="Nombre entendible para los usuarios."
    )
    texternal_fields = forms.CharField(
        label="Campos de la extracción",
        help_text="Se agregan los campos que pueden ser seleccionados del modelo.",
        widget=forms.Textarea(
            attrs={'class': 'form-control rc-external rc-external--field', 'readonly': True, "rows": "5"})
    )
    tfile_code = forms.CharField(
        label="Nombre de archivo",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-file'}),
        help_text="Nombre del archivo en formato CSV (Agregar extensión)"
    )
    file = forms.FileField(
        label="Archivo",
        widget=forms.FileInput(attrs={'class': 'form-control rc-file'}),
        help_text="Se carga el archivo con la base de datos en formato CSV"
    )
    tfile_fields = forms.CharField(
        label="Campos del archivo",
        help_text="Se agregan los campos que pueden ser seleccionados del modelo.",
        widget=forms.Textarea(
            attrs={'class': 'form-control rc-file rc-file--field', 'readonly': True,
                   "rows": "5"})
    )
    tapi_code = forms.CharField(
        label="Nombre del EndPoint",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-endpoint'}),
        help_text="Nombre del clave del EndPoint"
    )
    tapi_endpoint = forms.URLField(
        label="EndPoint",
        widget=forms.TextInput(attrs={'class': 'form-control rc-endpoint'}),
        help_text="Dirección completa del EndPoint que incluya el APIKey"
    )
    tapi_structure = forms.CharField(
        label="Estructura de JSON",
        help_text="Tienes que incluir el cuerpo del Response que será utilizado y denotar con : [] en el Key donde se obtendrán los datos.",
        widget=forms.Textarea(
            attrs={'class': 'form-control rc-endpoint ',
                   "rows": "5"})
    )
    tapi_fields = forms.CharField(
        label="Campos del archivo",
        help_text="Se agregan los campos que pueden ser seleccionados del modelo.",
        widget=forms.Textarea(
            attrs={'class': 'form-control rc-endpoint rc-endpoint--field', 'readonly': True,
                   "rows": "5"})
    )

    def __init__(self, *args, **kwargs):
        super(ModelsRule, self).__init__(*args, **kwargs)
        self.fields['tapi_fields'].required = False
        self.fields['tapi_endpoint'].required = False
        self.fields['tapi_code'].required = False
        self.fields['tapi_structure'].required = False
        self.fields['tfile_fields'].required = False
        self.fields['file'].required = False
        self.fields['tfile_code'].required = False
        self.fields['texternal_fields'].required = False
        self.fields['texternal_model'].required = False
        self.fields['texternal_code'].required = False
        self.fields['texternal_query'].required = False
        self.fields['texternal_db'].required = False
        self.fields['texternal_port'].required = False
        self.fields['texternal_password'].required = False
        self.fields['texternal_user'].required = False
        self.fields['texternal_host'].required = False
        self.fields['tinternal_fields'].required = False
        self.fields['tinternal_model'].required = False
        self.fields['tinternal_code'].required = False

    def clean_name(self):
        if Modru.objects.filter(name=self.cleaned_data['name']).exists():
            raise forms.ValidationError('El nombre del modelo ya ha sido registrado.')
        return self.cleaned_data['name']

    def save(self, user):
        print("********* [SAVE - START - MODEL]")
        data = self.cleaned_data
        if data["type"] == "internal":
            modelo = Modru(
                name = data["name"],
                description = data["description"],
                type = data["type"],
                tinternal_code = data["tinternal_code"],
                tinternal_model = data["tinternal_model"],
                tinternal_fields = data["tinternal_fields"],
                create_uid=user,
                write_uid=user
            )
            print(modelo)
            modelo.save()
        elif data["type"] == "external":
            modelo = Modru(
                name=data["name"],
                description=data["description"],
                type = data["type"],
                texternal_host=data["texternal_host"],
                texternal_user = data["texternal_user"],
                texternal_password = data["texternal_password"],
                texternal_port = data["texternal_port"],
                texternal_db = data["texternal_db"],
                texternal_query = data["texternal_query"],
                texternal_code = data["texternal_code"],
                texternal_model = data["texternal_model"],
                texternal_fields = data["texternal_fields"],
                create_uid=user,
                write_uid=user
            )
            print(modelo)
            modelo.save()
        elif data["type"] == "file":
            modelo = Modru(
                name=data["name"],
                description=data["description"],
                type=data["type"],
                tfile_code=data["tfile_code"],
                tfile_fields=data["tfile_fields"],
                tfile_path=str(data["file"].name),
                tfile_binary=data["file"],
                create_uid=user,
                write_uid=user
            )
            print(modelo)
            modelo.save()
        elif data["type"] == "api":
            modelo = Modru(
                name=data["name"],
                description=data["description"],
                type=data["type"],
                tapi_code=data["tapi_code"],
                tapi_endpoint=data["tapi_endpoint"],
                tapi_structure=data["tapi_structure"],
                tapi_fields=data["tapi_fields"],
                create_uid=user,
                write_uid=user
            )
            print(modelo)
            modelo.save()
        print("********* [SAVE - END - MODEL]")


class ModelsRuleUpdate(forms.Form):

    TYPE = Modru.TYPE

    id = forms.CharField(
        label="ID",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-id'})
    )
    name = forms.CharField(
        label="Nombre de Modelo",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-main', 'required': True}),
        help_text="Nombre legible para el usuario final"
    )
    description = forms.CharField(
        label="Descripción de Modelo",
        help_text="Describe la procedencia y el contexto del modelo.",
        widget=forms.Textarea(attrs={'class': 'form-control rc-main', 'required': True, "rows":"5"})
    )
    type = forms.ChoiceField(
        label="Tipo de modelo",
        choices=TYPE,
        widget=forms.Select(attrs={'class': 'form-control rc-main', 'required': True})
    )
    tinternal_code = forms.CharField(
        label="Nombre de tabla",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-internal rc-initial'}),
        help_text="Nombre de la tabla de la datos registrada en Roadly"
    )
    tinternal_model = forms.CharField(
        label="Nombre del modelo DJango",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-internal'}),
        help_text="Nombre del modelo de DJango registrado"
    )
    tinternal_fields = forms.CharField(
        label="Campos del modelo",
        help_text="Se agregan los campos que pueden ser seleccionados del modelo.",
        widget=forms.Textarea(attrs={'class': 'form-control rc-internal rc-internal--field', 'readonly': True, "rows": "5"})
    )
    texternal_host = forms.CharField(
        label="Host DB",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="DNS o IP de conexión a la base de datos de Postgres"
    )
    texternal_user = forms.CharField(
        label="Usuario DB",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="Usuario de la base de datos Postgres"
    )
    texternal_password = forms.CharField(
        label="Password DB",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="Password de la base de datos Postgres"
    )
    texternal_port = forms.CharField(
        label="Port DB",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="Puerto de la base de datos Postgres"
    )
    texternal_db = forms.CharField(
        label="Nombre DB",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="Nombre de la base de datos Postgres"
    )
    texternal_query = forms.CharField(
        label="Query de extracción",
        help_text="Se el Query de la extracción de base datos.",
        widget=forms.Textarea(
            attrs={'class': 'form-control rc-external', "rows": "5"})
    )
    texternal_code = forms.CharField(
        label="Nombre de tabla",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="Nombre de la tabla de la datos externa."
    )
    texternal_model = forms.CharField(
        label="Nombre de la Entidad o Vista",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-external'}),
        help_text="Nombre entendible para los usuarios."
    )
    texternal_fields = forms.CharField(
        label="Campos de la extracción",
        help_text="Se agregan los campos que pueden ser seleccionados del modelo.",
        widget=forms.Textarea(
            attrs={'class': 'form-control rc-external rc-external--field', "rows": "5"})
    )
    tfile_code = forms.CharField(
        label="Nombre de archivo",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-file'}),
        help_text="Nombre del archivo en formato CSV (Agregar extensión)"
    )
    tfile_path = forms.CharField(
        label="Nombre de archivo (Carga)",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-file'}),
        help_text="Nombre guardado desde la carga del Archivo"
    )
    file = forms.CharField(
        label="Archivo",
        widget=forms.TextInput(attrs={'class': 'form-control rc-file'}),
        help_text="Se carga el archivo con la base de datos en formato CSV"
    )
    tfile_fields = forms.CharField(
        label="Campos del archivo",
        help_text="Se agregan los campos que pueden ser seleccionados del modelo.",
        widget=forms.Textarea(
            attrs={'class': 'form-control rc-file rc-file--field', "rows": "5"})
    )
    tapi_code = forms.CharField(
        label="Nombre del EndPoint",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-endpoint'}),
        help_text="Nombre del clave del EndPoint"
    )
    tapi_endpoint = forms.URLField(
        label="EndPoint",
        widget=forms.TextInput(attrs={'class': 'form-control rc-endpoint'}),
        help_text="Dirección completa del EndPoint que incluya el APIKey"
    )
    tapi_structure = forms.CharField(
        label="Estructura de JSON",
        help_text="Tienes que incluir el cuerpo del Response que será utilizado y denotar con : [] en el Key donde se obtendrán los datos.",
        widget=forms.Textarea(
            attrs={'class': 'form-control rc-endpoint ',
                   "rows": "5"})
    )
    tapi_fields = forms.CharField(
        label="Campos del archivo",
        help_text="Se agregan los campos que pueden ser seleccionados del modelo.",
        widget=forms.Textarea(
            attrs={'class': 'form-control rc-endpoint rc-endpoint--field', "rows": "5"})
    )

    def __init__(self, *args, **kwargs):
        super(ModelsRuleUpdate, self).__init__(*args, **kwargs)
        self.fields['tapi_fields'].required = False
        self.fields['tapi_endpoint'].required = False
        self.fields['tapi_code'].required = False
        self.fields['tapi_structure'].required = False
        self.fields['tfile_fields'].required = False
        self.fields['file'].required = False
        self.fields['tfile_code'].required = False
        self.fields['tfile_path'].required = False
        self.fields['texternal_fields'].required = False
        self.fields['texternal_model'].required = False
        self.fields['texternal_code'].required = False
        self.fields['texternal_query'].required = False
        self.fields['texternal_db'].required = False
        self.fields['texternal_port'].required = False
        self.fields['texternal_password'].required = False
        self.fields['texternal_user'].required = False
        self.fields['texternal_host'].required = False
        self.fields['tinternal_fields'].required = False
        self.fields['tinternal_model'].required = False
        self.fields['tinternal_code'].required = False

    def write(self, user):
        import datetime as d
        print("********* [WRITE - START - MODEL]")
        data = self.cleaned_data
        if data["type"] == "internal":
            modelo = Modru.objects.filter(id=data["id"]).all()[0]
            print("****")
            modelo.name = data["name"]
            modelo.description = data["description"]
            modelo.type = data["type"]
            modelo.tinternal_code = data["tinternal_code"]
            modelo.tinternal_model = data["tinternal_model"]
            modelo.tinternal_fields = data["tinternal_fields"]
            modelo.write_uid = user
            modelo.write_data = d.datetime.today()
            print(modelo)
            modelo.save()
        elif data["type"] == "external":
            modelo = Modru.objects.filter(id=data["id"]).all()[0]
            print("****")
            modelo.name = data["name"]
            modelo.description = data["description"]
            modelo.type = data["type"]
            modelo.texternal_host = data["texternal_host"]
            modelo.texternal_user = data["texternal_user"]
            modelo.texternal_password = data["texternal_password"]
            modelo.texternal_port = data["texternal_port"]
            modelo.texternal_db = data["texternal_db"]
            modelo.texternal_query = data["texternal_query"]
            modelo.texternal_code = data["texternal_code"]
            modelo.texternal_model = data["texternal_model"]
            modelo.texternal_fields = data["texternal_fields"]
            modelo.write_uid = user
            modelo.write_data = d.datetime.today()
            print(modelo)
            modelo.save()
        elif data["type"] == "file":
            modelo = Modru.objects.filter(id=data["id"]).all()[0]
            print("****")
            modelo.name = data["name"]
            modelo.description = data["description"]
            modelo.type = data["type"]
            modelo.tfile_code = data["tfile_code"]
            modelo.tfile_fields = data["tfile_fields"]
            modelo.tfile_path = data["tfile_path"]
            modelo.tfile_binary = data["file"]
            modelo.write_uid = user
            modelo.write_data = d.datetime.today()
            print(modelo)
            modelo.save()
        elif data["type"] == "api":
            modelo = Modru.objects.filter(id=data["id"]).all()[0]
            print("****")
            modelo.name = data["name"]
            modelo.description = data["description"]
            modelo.type = data["type"]
            modelo.tapi_code = data["tapi_code"]
            modelo.tapi_endpoint = data["tapi_endpoint"]
            modelo.tapi_fields = data["tapi_fields"]
            modelo.tapi_structure = data["tapi_structure"]
            modelo.write_uid = user
            modelo.write_data = d.datetime.today()
            print(modelo)
            modelo.save()
        print("********* [WRITE - END - MODEL]")

class HeaderRule(forms.Form):

    TYPE = Cond.TYPE
    ACTION = Cond.ACTION
    EVAL = Cond.RULE_EVAL
    CHOICE = [('0', '')]
    EVALOUT = Cond.EVAL
    COMP = [
        ('',''),
        ('and','AND'),
        ('or','OR'),
    ]

    def __init__(self, *args, **kwargs):
        super(HeaderRule, self).__init__(*args, **kwargs)
        current_fields = Modru.objects.filter(tinternal_code="current").values("tinternal_fields")[0]["tinternal_fields"]
        current_id = Modru.objects.filter(tinternal_code="current").values("id")[0]["id"]
        current_code = Modru.objects.filter(tinternal_code="current").values("tinternal_model")[0]["tinternal_model"]
        array_fields = current_fields.split(",")
        CHOICE1 = [(q, q) for q in array_fields]
        self.fields['tcurrent_id'].initial = current_id
        self.fields['tcurrent_code'].initial = current_code
        self.fields['tcurrent_fields'].choices = CHOICE1
        models_rules = Modru.objects.all().values()
        print("--------------------->")
        array_mr = []
        array_mr_v = []
        intx = 0
        idx = 0
        for mr in models_rules:
            if mr['type'] == 'internal':
                code = mr['tinternal_code']
            elif mr['type'] == 'external':
                code = mr['texternal_code']
            elif mr['type'] == 'file':
                code = mr['tfile_code']
            elif mr['type'] == 'api':
                code = mr['tapi_code']
            if intx == 0:
                idx = mr['id']
                if mr['type'] == 'internal':
                    fields = mr['tinternal_fields']
                elif mr['type'] == 'external':
                    fields = mr['texternal_fields']
                elif mr['type'] == 'file':
                    fields = mr['tfile_fields']
                elif mr['type'] == 'api':
                    fields = mr['tapi_fields']
            array_mr.append([mr['id'], "[{}] {}".format(code,mr['name'])])
            intx = intx + 1
        CHOICE2 = [(q[0], q[1]) for q in array_mr]
        CHOICE3 = [(q, q) for q in fields.split(',')]
        self.fields['tmodel_code'].choices = CHOICE2
        self.fields['amodel_code'].choices = CHOICE2
        self.fields['tmodel_field'].choices = CHOICE3
        self.fields['amodel_field'].choices = CHOICE3
        self.fields['tmodel_id'].initial = idx
        self.fields['amodel_id'].initial = idx
        self.fields['name'].required = False
        self.fields['description'].required = False
        self.fields['code'].required = False
        self.fields['typec'].required = False
        self.fields['tcurrent_id'].required = False
        self.fields['tcurrent_code'].required = False
        self.fields['tcurrent_fields'].required = False
        self.fields['tmodel_id'].required = False
        self.fields['tmodel_code'].required = False
        self.fields['tmodel_field'].required = False
        self.fields['tmodel_fields'].required = False
        self.fields['tmodels_id'].required = False
        self.fields['tmodels_code'].required = False
        self.fields['tmodels_fields'].required = False
        self.fields['tseed_id'].required = False
        self.fields['tseed_code'].required = False
        self.fields['action'].required = False
        self.fields['eval'].required = False
        self.fields['avalue'].required = False
        self.fields['avaluescomp'].required = False
        self.fields['avalues'].required = False
        self.fields['afield'].required = False
        self.fields['afieldscomp'].required = False
        self.fields['afields'].required = False
        self.fields['amodel_id'].required = False
        self.fields['amodel_code'].required = False
        self.fields['amodel_field'].required = False
        self.fields['amodel_fieldscomp'].required = False
        self.fields['amodel_fields'].required = False
        self.fields['evalout'].required = False
        print("<---------------------")

    # ------------------------ CONDITION
    name = forms.CharField(
        label="Nombre de Condición",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-main', 'required': True}),
        help_text="Nombre legible para el usuario final"
    )
    description = forms.CharField(
        label="Descripción de Condición",
        help_text="Describe la procedencia y el contexto de la condición.",
        widget=forms.Textarea(attrs={'class': 'form-control rc-main', 'required': True, "rows": "5"})
    )
    code = forms.CharField(
        label="Codigo de la condición",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control rc-main', 'required': True}),
        help_text="Nombre técnico de la condición"
    )
    typec = forms.ChoiceField(
        label="Tipo de condición",
        choices=TYPE,
        widget=forms.Select(attrs={'class': 'form-control rc-main', 'required': True})
    )
    # ------------------------ CONDITION
    # ------------------------ MODEL
    # --- CURRENT
    tcurrent_id = forms.CharField(
        label="ID Modelo concurrente",
        widget=forms.TextInput(attrs={'class': 'form-control rc-type-action rc-current'}),
        help_text="Id de la tabla concurrente"
    )
    tcurrent_code = forms.CharField(
        label="Codigo Modelo concurrente",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-type-action rc-current'}),
        help_text="Codigo de la tabla concurrente"
    )
    tcurrent_fields = forms.ChoiceField(
        label="Campos del modelo concurrente",
        choices=CHOICE,
        widget=forms.Select(attrs={'class': 'form-control rc-type-action rc-current'})
    )
    # --- MODEL
    tmodel_id = forms.CharField(
        label="Id modelo (Modelo Agregado)",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-type-action rc-model'}),
        help_text="Id de los modelos seleccionables dados de alta."
    )
    tmodel_code = forms.ChoiceField(
        label="Modelo (Modelo Agregado)",
        choices=CHOICE,
        widget=forms.Select(attrs={'class': 'form-control rc-type-action rc-model tmodel_code'})
    )
    tmodel_field = forms.ChoiceField(
        label="Campo del modelo (Modelo Agregado)",
        choices=CHOICE,
        widget=forms.Select(attrs={'class': 'form-control rc-type-action rc-model tmodel_field'})
    )
    tmodel_fields = forms.CharField(
        label="Campos del modelo (Modelo Agregado)",
        help_text="Son los valores de campos que se van agregando adicionales para la evaluación",
        widget=forms.Textarea(attrs={'class': 'form-control rc-type-action rc-model btn_tmodel_fields', "rows": "5", "disabled":True})
    )
    # --- MODELS
    tmodels_id = forms.CharField(
        label="Ids del modelos (Modelos Agregado)",
        help_text="Id de modelos seleccionados del modelo (Modelos Agregados)",
        widget=forms.Textarea(attrs={'class': 'form-control rc-type-action rc-models', "rows": "5", "disabled":True })
    )
    tmodels_code = forms.CharField(
        label="Codigos de modelos (Modelos Agregado)",
        help_text="Codigos de los modelos seleccionados del modelo (Modelos Agregados)",
        widget=forms.Textarea(attrs={'class': 'form-control rc-type-action rc-models', "rows": "5", "disabled":True })
    )
    tmodels_fields = forms.CharField(
        label="Campos de modelos (Modelos Agregado)",
        help_text="Campos de los modelos seleccionados del modelo (Modelos Agregados)",
        widget=forms.Textarea(attrs={'class': 'form-control rc-type-action rc-models', "rows": "5", "disabled":True })
    )
    # --- seed
    tseed_id = forms.CharField(
        label="Id de la semilla(Seed)",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-type-action rc-seed'}),
        help_text="Id de las semillas seleccionables."
    )
    tseed_code = forms.ChoiceField(
        label="Semillas seleccionables",
        choices=CHOICE,
        widget=forms.Select(attrs={'class': 'form-control rc-type-action rc-seed'})
    )
    # ------------------------ MODEL
    # ------------------------ EVAL
    action = forms.ChoiceField(
        label="Tipo de evaluación",
        choices=ACTION,
        widget=forms.Select(attrs={'class': 'form-control rc-eval rc-eval-primary', 'required': True})
    )
    eval = forms.ChoiceField(
        label="Clase de evaluación",
        choices=EVAL,
        widget=forms.Select(attrs={'class': 'form-control rc-eval rc-eval-second', 'required': True})
    )
    # ------------------------ EVAL
    # ------------------------ EVAL ONE VALUE, MORE VALUES
    avalue = forms.CharField(
        label="Valor a evaluar",
        widget=forms.TextInput(attrs={'class': 'form-control rx-eval rav-value', 'visible': True }),
        help_text="Agrega el valor a evaluar de la condición"
    )
    avaluescomp = forms.ChoiceField(
        label="Tipo de compuerta (Valores)",
        choices=COMP,
        widget=forms.Select(attrs={'class': 'form-control rx-eval rav-values-comp', 'visible': False})
    )
    avalues = forms.CharField(
        label="Valores a evaluar",
        help_text="Valores de evaluación para las condiciones",
        widget=forms.Textarea(
            attrs={'class': 'form-control rx-eval rav-values', "rows": "5", 'visible': True, "disabled": True})
    )
    # ------------------------ FIELD
    afield = forms.ChoiceField(
        label="Campo a evaluar",
        choices=CHOICE,
        widget=forms.Select(attrs={'class': 'form-control rx-eval rav-field'})
    )
    afieldscomp = forms.ChoiceField(
        label="Tipo de compuerta (Campos)",
        choices=COMP,
        widget=forms.Select(attrs={'class': 'form-control rx-eval rav-fields-comp', 'visible': False})
    )
    afields = forms.CharField(
        label="Campos a evaluar",
        help_text="Campos para evaluación de las condiciones",
        widget=forms.Textarea(attrs={'class': 'form-control rx-eval rav-fields', "rows": "5", 'visible': True, "disabled":True})
    )
    # ------------------------ MODEL
    amodel_id = forms.CharField(
        label="Id modelo (Modelo Agregado)",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rx-eval rav-model'}),
        help_text="Id de los modelos seleccionables dados de alta."
    )
    amodel_code = forms.ChoiceField(
        label="Modelo (Modelo Agregado)",
        choices=CHOICE,
        widget=forms.Select(attrs={'class': 'form-control rx-eval rav-model amodel_code'})
    )
    amodel_field = forms.ChoiceField(
        label="Campo del modelo (Modelo Agregado)",
        choices=CHOICE,
        widget=forms.Select(attrs={'class': 'form-control rx-eval rav-model amodel_field'})
    )
    amodel_fieldscomp = forms.ChoiceField(
        label="Tipo de compuerta (Modelo)",
        choices=COMP,
        widget=forms.Select(attrs={'class': 'form-control rx-eval rav-model-comp', 'visible': False})
    )
    amodel_fields = forms.CharField(
        label="Campos de modelos (Modelos Agregado)",
        help_text="Campos de los modelos seleccionados del modelo (Modelos Agregados)",
        widget=forms.Textarea(attrs={'class': 'form-control rx-eval rav-model amodel_field', "rows": "5", "disabled": True})
    )
    # ------------------------ EVAL ONE VALUE, MORE VALUES
    evalout = forms.ChoiceField(
        label="Acción a ejecutar",
        choices=EVALOUT,
        widget=forms.Select(attrs={'class': 'form-control rz-eval'})
    )
