from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()
import re


class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_password = forms.CharField(widget=forms.PasswordInput)
    telefono = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['username', 'email', 'telefono', 'password', 'confirmar_password']

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Validar longitud
        if len(password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')

        # Validar mayúsculas
        if not re.search(r'[A-Z]', password):
            raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')

        # Validar minúsculas
        if not re.search(r'[a-z]', password):
            raise ValidationError('La contraseña debe contener al menos una letra minúscula.')

        # Validar números
        if not re.search(r'[0-9]', password):
            raise ValidationError('La contraseña debe contener al menos un número.')

        # Validar símbolos especiales
        if not re.search(r'[\W_]', password):
            raise ValidationError('La contraseña debe contener al menos un carácter especial (como !@#$%).')

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar_password = cleaned_data.get('confirmar_password')

        if password and confirmar_password and password != confirmar_password:
            raise ValidationError('Las contraseñas no coinciden.')

        # Validar número de teléfono (solo 10 dígitos)
        telefono = cleaned_data.get('telefono')
        if telefono and not re.fullmatch(r'\d{10}', telefono):
            raise ValidationError('El número de teléfono debe tener exactamente 10 dígitos.')

        return cleaned_data


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
