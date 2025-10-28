from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from applications.Usuarios.models import Usuario
from .forms import RegistroForm,LoginForm 
from django.contrib import messages
from .forms import LoginForm  



# Create your views here.

class RegisterView(CreateView):
    form_class = RegistroForm
    template_name = 'login/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        nombre = form.cleaned_data.get('nombre')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password') 
        
        Usuario.objects.create_user(
            email=email,
            nombre=nombre,
            password=password
        )
        return super().form_valid(form)




class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login/login.html'
    # Define la URL a la que irás si el inicio de sesión es exitoso
    success_url = reverse_lazy('main') 

    def form_valid(self, form):

        email_ingresado = form.cleaned_data.get('email')
        password_ingresada = form.cleaned_data.get('password')
        user = authenticate(
            self.request, 
            email=email_ingresado,  # Usa el campo que tu backend espera
            password=password_ingresada
        )
        # 3. Lógica de Respuesta
        if user is not None:
            login(self.request, user)
            return super().form_valid(form) # Redirige solo si autentica
        else:
            messages.error(self.request, 'Correo de usuario o contraseña incorrectos.')
            return self.form_invalid(form) # Si no autentica, vuelve a cargar el formulario
            # Vuelve a renderizar la plantilla, mostrando el formulario con errores
        return super().form_invalid(form)




