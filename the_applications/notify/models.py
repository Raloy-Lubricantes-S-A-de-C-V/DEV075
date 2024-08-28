from django.contrib.auth.models import User
from django.db import models

class TypeNotify(models.Model):
    name = models.CharField(max_length=50, default='')
    color = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=400, default='')
    active =models.SmallIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Notify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(TypeNotify, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=400, default='')
    active = models.SmallIntegerField(default=1)
    see = models.SmallIntegerField(default=0)
    important = models.SmallIntegerField(default=0)
    trash = models.SmallIntegerField(default=0)
    to = models.SmallIntegerField(default=1)
    priority = models.SmallIntegerField(default=0)
    picture = models.ImageField(upload_to='notify/pictures',
                                blank=True,
                                null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name