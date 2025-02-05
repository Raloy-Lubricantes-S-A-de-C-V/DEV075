from django.contrib.auth.models import User
from django.db import models


class Transport(models.Model):
    name = models.CharField(max_length=100, default='')
    volumen = models.FloatField("Volumén", default=0.0)  #
    capacity_pallet = models.FloatField("Capacidad de tarimas", default=0.0)  #
    active = models.SmallIntegerField(default=1)
    write_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_uid = models.IntegerField()
    write_uid = models.IntegerField()