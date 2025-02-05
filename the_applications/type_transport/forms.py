"""Apps forms."""
import os
# Django
from django import forms
from the_applications.type_transport.models import Transport as T


class TypeTransoportForms(forms.Form):

    id = forms.CharField(
        label="ID",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rc-main', 'hidden':True})
    )
    name = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        help_text="Nombre del tipo de transporte"
    )
    volumen = forms.FloatField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
        help_text = "Volumén total en litros"
    )
    capacity_pallet = forms.FloatField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
        help_text = "Capacidad por tarimas del producto"
    )

    def __init__(self, *args, **kwargs):
        super(TypeTransoportForms, self).__init__(*args, **kwargs)
        self.fields['id'].required = False

    def clean_name(self):
        if T.objects.filter(name=self.cleaned_data['name']).exists():
            raise forms.ValidationError('El nombre del modelo ya ha sido registrado.')
        return self.cleaned_data['name']

    def save(self,user):
        print("********* [SAVE - START - MODEL]")
        data = self.cleaned_data
        transporte = T(
            name=data['name'],
            volumen=data['volumen'],
            capacity_pallet=data['capacity_pallet'],
            create_uid=user,
            write_uid=user
        )
        transporte.save()
        print("********* [SAVE - END - MODEL]")
    def write(self,user):
        print("********* [SAVE - START - MODEL]")
        data = self.cleaned_data
        print(data)
        modelo = T.objects.filter(id=data["id"]).all()[0]
        modelo.name = data['name']
        modelo.volumen = data['volumen']
        modelo.capacity_pallet = data['capacity_pallet']
        modelo.write_uid = user
        modelo.save()
        print("********* [SAVE - END - MODEL]")



