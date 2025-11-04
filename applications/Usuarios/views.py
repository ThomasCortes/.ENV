from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from applications.Usuarios.models import Usuario
from .forms import RegistroForm,LoginForm 
from django.contrib import messages
from .forms import LoginForm  



# Create your views here.
class RegisterView(CreateView):
    form_class = RegistroForm
    template_name = 'login/register.html'
    success_url = reverse_lazy('cuestionario')

    def form_valid(self, form):
        nombre = form.cleaned_data.get('nombre')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = Usuario.objects.create_user(
            nombre=nombre,
            email=email,
            password=password
        )
        # 🟢 Solución: Especificar el backend personalizado
        # Usamos la ruta exacta que definiste en settings.py para el login automático.
        login(
            self.request, 
            user, 
            backend='applications.Usuarios.backends.CustomAuthBackend' 
        )
        # Continuar con el flujo normal (redirige al cuestionario)
        return redirect('cuestionario')

# Define la ruta de tu backend personalizado (Asegúrate de que esta sea la correcta)
CUSTOM_BACKEND = 'applications.Usuarios.backends.CustomAuthBackend'

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login/login.html'
    success_url = reverse_lazy('main') 

    def form_valid(self, form):
        email_ingresado = form.cleaned_data.get('email')
        password_ingresada = form.cleaned_data.get('password')
        
        # 1. Autenticación:
        # 'authenticate' probará todos los backends, incluyendo el personalizado.
        user = authenticate(
            self.request, 
            email=email_ingresado, 
            password=password_ingresada
        )
        
        # 2. Lógica de Respuesta
        if user is not None:
            # 🟢 CORRECCIÓN CLAVE: Especificar el backend para que Django sepa 
            # cómo mantener la sesión activa sin ambigüedad.
            login(self.request, user, backend=CUSTOM_BACKEND)
            return super().form_valid(form) # Redirige a success_url ('main')
        else:
            # Si no autentica, añade un mensaje de error
            messages.error(self.request, 'Correo de usuario o contraseña incorrectos.')
            
            # Vuelve a renderizar el formulario con los errores
            return self.form_invalid(form)



