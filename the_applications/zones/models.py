from django.db import models


class Model(models.Model):
    name = models.CharField(max_length=200, default='')
    description = models.TextField()
    edos = models.CharField(max_length=200, default='')
    code = models.CharField(max_length=200, default='')
    number_code = models.IntegerField()
    active = models.SmallIntegerField(default=1)
    write_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_uid = models.IntegerField()
    write_uid = models.IntegerField()

class Edos(models.Model):
    name = models.CharField(max_length=200, default='')
    active = models.SmallIntegerField(default=1)
    write_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_uid = models.IntegerField()
    write_uid = models.IntegerField()