from django.contrib.auth.models import User
from django.db import models


class Model(models.Model):
    TYPE = [
        ("internal", "Interno"),
        ("external", "Postgresql"),
        ("file", "CSV"),
        ("api", "API"),
    ]
    STATUS = [
        ("ready", "Listo"),
        ("used", "En uso"),
    ]
    name = models.CharField(max_length=100, default='')
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE, default="internal")
    status = models.CharField(max_length=20, choices=STATUS, default="ready")
    tinternal_code = models.CharField(max_length=100, default='')
    tinternal_model = models.CharField(max_length=100, default='')
    tinternal_fields = models.TextField()
    texternal_host = models.CharField(max_length=100, default='')
    texternal_user = models.CharField(max_length=100, default='')
    texternal_password = models.CharField(max_length=100, default='')
    texternal_port = models.CharField(max_length=100, default='')
    texternal_db = models.CharField(max_length=100, default='')
    texternal_query = models.TextField()
    texternal_code = models.CharField(max_length=100, default='')
    texternal_model = models.CharField(max_length=100, default='')
    texternal_fields = models.TextField()
    tfile_code = models.CharField(max_length=100, default='')
    tfile_fields = models.TextField()
    tfile_path = models.TextField()
    tfile_binary = models.FileField(upload_to='file', max_length = 500)
    tapi_code = models.CharField(max_length=100, default='')
    tapi_fields = models.TextField()
    tapi_structure = models.TextField(default='')
    tapi_endpoint = models.TextField()
    active = models.SmallIntegerField(default=1)
    delete = models.SmallIntegerField(default=0)
    write_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_uid = models.IntegerField()
    write_uid = models.IntegerField()

class Header(models.Model):
    TYPE=[
        ("current","Actual"),
        ("model","Modelo"),
        ("models","Modelos"),
        ("semilla","Semilla"),
    ]
    ACTION = [
        ("equal", "Igual a"),
        ("greaterthan", "Mayor que"),
        ("lessthan", "Menor que"),
        ("contain", "Contiene"),
        ("notcontain", "No contiene"),
        ("lefteq", "Empieza con"),
        ("rigtheq", "Termina con"),
        ("notdefined", "No definido"),
        ("defined", "Definido"),
    ]
    RULE_EVAL = [
        ("value", "Valor"),
        ("values", "Valores"),
        ("field", "Campo"),
        ("fields", "Campos"),
        ("model", "Modelo"),
    ]
    EVAL = [
        ("omit", "Omitir"),
        ("perm", "Permancer"),
        ("group", "Agrupar"),
        ("categ", "Categorizar"),
        ("seed", "Semilla"),
    ]
    name = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=50, default='')
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE, default="current")
    tcurrent_id = models.IntegerField()
    tcurrent_code = models.CharField(max_length=100, default='')
    tcurrent_fields = models.TextField()
    tmodel_id = models.IntegerField()
    tmodel_code = models.CharField(max_length=100, default='')
    tmodel_field = models.CharField(max_length=100, default='')
    tmodel_fields = models.TextField()
    tmodels_id = models.TextField()
    tmodels_code = models.TextField()
    tmodels_fields = models.TextField()
    tseed_id = models.IntegerField()
    tseed_code = models.TextField()
    action = models.CharField(max_length=20, choices=ACTION, default="equal")
    eval = models.CharField(max_length=20, choices=RULE_EVAL, default="value")
    avalue = models.CharField(max_length=500, default='')
    avaluescomp = models.TextField(default="")
    avalues = models.TextField()
    afield = models.CharField(max_length=200, default='')
    afieldscomp = models.TextField(default="")
    afields = models.TextField()
    amodel_id = models.IntegerField()
    amodel_code = models.CharField(max_length=100, default='')
    amodel_field = models.CharField(max_length=100, default='')
    amodel_fields = models.TextField()
    amodel_fieldscomp = models.TextField(default="")
    active = models.SmallIntegerField(default=1)
    write_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_uid = models.IntegerField()
    write_uid = models.IntegerField()
