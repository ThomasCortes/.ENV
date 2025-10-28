from django import forms
from .models import Usuario

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'password', 'numero_telefono']


class LoginForm(forms.Form ):

    email = forms.CharField(
        label='email',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
