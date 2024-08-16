"""User forms."""

# Django
from django import forms

# Models
from django.contrib.auth.models import User
from .models import Profile


class SignupForm(forms.Form):
    """Sign up form."""

    username = forms.CharField(label=False,
                               min_length=4,
                               max_length=50,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Nombre de usuario', 'class': 'form-control',
                                          'required': True}))

    password = forms.CharField(
        label=False,
        max_length=70,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control', 'required': True}))

    password_confirmation = forms.CharField(
        label=False,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirma Contraseña', 'class': 'form-control', 'required': True}))

    first_name = forms.CharField(min_length=2, max_length=50, widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Primer Nombre'}),label=False)
    last_name = forms.CharField(min_length=2, max_length=50, widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Apellidos'}), label=False)

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(attrs={"class":"form-control",'placeholder': 'Email'}),
        label=False
    )

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_query = User.objects.filter(username=username).exists()
        if username_query:
            raise forms.ValidationError('Este usuario ya ha sido utilizado.')
        return username

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('La contraseña no es correcta')

        return data

    def save(self):
        """Create user and profile."""
        data = self.cleaned_data
        print(data)
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()


themes ={
    ('apple', 'apple'),
    ('default', 'default'),
    ('facebook', 'facebook'),
    ('material', 'material'),
    ('transparent', 'transparent'),
    ('google', 'google'),
}

class ProfileForm(forms.Form):
    """Profile form."""
    biography = forms.CharField(max_length=500, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    theme = forms.CharField(widget=forms.Select(choices=themes))
    picture = forms.ImageField(required=False)
