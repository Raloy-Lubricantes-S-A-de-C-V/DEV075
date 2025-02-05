"""Apps forms."""
import os
# Django
from django import forms
from the_applications.zones.models import Model as M, Edos as E

class EdosForms(forms.Form):

    id = forms.CharField(
        label="ID",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-main', 'hidden': True})
    )

    name = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        help_text="Nombre del estado"
    )
    def __init__(self, *args, **kwargs):
        super(EdosForms, self).__init__(*args, **kwargs)
        self.fields['id'].required = False

    def clean_name(self):
        if E.objects.filter(name=self.cleaned_data['name']).exists():
            raise forms.ValidationError('El nombre del modelo ya ha sido registrado.')
        return self.cleaned_data['name']

    def save(self,user):
        print("********* [CREATE - START - MODEL]")
        data = self.cleaned_data
        edos = E(
            name=data['name'],
            create_uid=user,
            write_uid=user
        )
        edos.save()
        print(data)
        print("********* [CREATE - END - MODEL]")
    def write(self,user):
        print("********* [SAVE - START - MODEL]")
        data = self.cleaned_data
        print(data)
        modelo = E.objects.filter(id=data["id"]).all()[0]
        modelo.name = data['name']
        modelo.write_uid = user
        modelo.save()
        print("********* [SAVE - END - MODEL]")

class ModelForms(forms.Form):

    id = forms.CharField(
        label="ID",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-main', 'hidden':True})
    )
    name = forms.CharField(
        label="Nombre",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        help_text="Nombre del estado"
    )
    description = forms.CharField(
        label="Descripción la zona",
        help_text="Describe la zona",
        widget=forms.Textarea(attrs={'class': 'form-control rc-main', 'required': True, "rows": "5"})
    )
    edos = forms.CharField(
        label="Estados",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control col-9 edos-z', 'required': True}),
        help_text="Listado de estados que abarca"
    )
    code = forms.CharField(
        label="Codigo siplificado hexadecimal",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        help_text="Codigo corto hexadecimal"
    )
    number_code = forms.FloatField(
        required=True, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
        help_text = "Codigo corto numerico"
    )

    def __init__(self, *args, **kwargs):
        super(ModelForms, self).__init__(*args, **kwargs)
        self.fields['id'].required = False

    def clean_name(self):
        if M.objects.filter(name=self.cleaned_data['name']).exists():
            raise forms.ValidationError('El nombre del modelo ya ha sido registrado.')
        return self.cleaned_data['name']

    def save(self,user):
        print("********* [SAVE - START - MODEL]")
        data = self.cleaned_data
        modl = M(
            name=data['name'],
            description=data['description'],
            edos=data['edos'],
            code=data['code'],
            number_code=data['number_code'],
            create_uid=user,
            write_uid=user
        )
        modl.save()
        print(data)
        print("********* [SAVE - END - MODEL]")

class ModelForms2(forms.Form):

    id = forms.CharField(
        label="ID",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-main', 'hidden':True})
    )
    name = forms.CharField(
        label="Nombre",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        help_text="Nombre del estado"
    )
    description = forms.CharField(
        label="Descripción la zona",
        help_text="Describe la zona",
        widget=forms.Textarea(attrs={'class': 'form-control rc-main', 'required': True, "rows": "5"})
    )
    edos = forms.CharField(
        label="Estados",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control col-9 edos-z', 'required': True}),
        help_text="Listado de estados que abarca"
    )
    code = forms.CharField(
        label="Codigo siplificado hexadecimal",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        help_text="Codigo corto hexadecimal"
    )
    number_code = forms.FloatField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
        help_text = "Codigo corto numerico"
    )

    def __init__(self, *args, **kwargs):
        super(ModelForms2, self).__init__(*args, **kwargs)
        self.fields['id'].required = False
    def write(self,user):
        print("********* [SAVE - START - MODEL]")
        data = self.cleaned_data
        print(data)
        modelo = M.objects.filter(id=data["id"]).all()[0]
        modelo.name = data['name']
        modelo.description = data['description']
        modelo.edos = data['edos']
        modelo.code = data['code']
        modelo.number_code = data['number_code']
        modelo.write_uid = user
        modelo.save()
        print("********* [SAVE - END - MODEL]")



