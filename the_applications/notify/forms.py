"""Apps forms."""
import os
# Django
from django import forms
from the_applications.notify.models import TypeNotify, Notify
from django.contrib.auth.models import User

class TypeNotifyForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    color = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=400, required=False)

    def clean_name(self):
        if not self.cleaned_data['name']:
            raise forms.ValidationError('Es obligatorio poner un "nombre"')
        return self.cleaned_data['name']

    def clean_color(self):
        if not self.cleaned_data['color']:
            raise forms.ValidationError('Es obligatorio poner un "color"')
        return self.cleaned_data['color']

    def save(self):
        data = self.cleaned_data
        print("-------------------------------------------- [SAVE] ->")
        type = TypeNotify()
        type.name = data["name"]
        type.color = data["color"]
        type.description = data["description"]
        print(type)
        type.save()
        print("-------------------------------------------- [SAVE] <-")

class NotifyForm(forms.Form):

    user = forms.IntegerField(required=True)
    type = forms.IntegerField(required=True)
    name = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=400, required=True)
    priority = forms.IntegerField(required=True)
    picture = forms.CharField(max_length=400, required=False)

    def clean_user(self):
        if not self.cleaned_data['user']:
            raise forms.ValidationError('Es obligatorio seleccionar un "usuario" para la notificación')
        return self.cleaned_data['user']
    def clean_type(self):
        if not self.cleaned_data['type']:
            raise forms.ValidationError('Es obligatorio seleccionar un "tipo" de notificación')
        return self.cleaned_data['type']
    def clean_name(self):
        if not self.cleaned_data['name']:
            raise forms.ValidationError('Es obligatorio poner un "nombre"')
        return self.cleaned_data['name']

    def clean_description(self):
        if not self.cleaned_data['description']:
            raise forms.ValidationError('Es obligatorio poner una "descripción"')
        return self.cleaned_data['description']

    def clean_priority(self):
        if not self.cleaned_data['priority']:
            raise forms.ValidationError('Es obligatorio poner la "prioridad" de la notificación')
        return self.cleaned_data['priority']

    def save(self, data):
        print("-------------------------------------------- [SAVE] ->")
        print(data)
        notify = Notify()
        notify.name = data['name']
        notify.user = User.objects.get(id=data['user'])
        notify.type = TypeNotify.objects.get(id=data['type'])
        notify.to = data['from']
        notify.description = data['description']
        notify.priority = data['priority']
        if data['picture']:
            notify.picture = data['picture']
        notify.save()
        print("-------------------------------------------- [SAVE] <-")
