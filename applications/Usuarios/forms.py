from django import forms
from .models import Usuario

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'password', 'numero_telefono']

class LoginForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'password']
