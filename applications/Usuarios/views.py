from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, FormView,TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from applications.Usuarios.models import Usuario
from .forms import RegistroForm,LoginForm
from django.contrib import messages
from .forms import LoginForm  
#NUEVAS IMPORTACIONES
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import PasswordResetCode
from django.conf import settings
#OTRO NUEVO

#MAS CLASES
def send_verification_code(request):
    """Vista para solicitar el correo y enviar el código de recuperación"""
    if request.method == 'POST':
        email = request.POST.get('email')

        # Verificar si el correo existe
        if not Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El correo no está registrado.')
            return redirect('send_verification_code')

        # Generar código de 6 dígitos
        code = str(random.randint(100000, 999999))

        # Guardar código y correo en la sesión
        request.session['verification_code'] = code
        request.session['email'] = email

        # Enviar el correo con el código
        send_mail(
            'Código de recuperación',
            f'Tu código de recuperación es: {code}',
            settings.EMAIL_HOST_USER,  # Desde el correo configurado
            [email],                   # Destinatario
            fail_silently=False,
        )

        messages.success(request, 'Código enviado a tu correo.')
        return redirect('verify_code')  # Página para ingresar el código

    return render(request, 'recuperar/recuperar_contraseña.html')


def verify_code(request):
    """Vista para ingresar y validar el código de recuperación"""
    if request.method == 'POST':
        input_code = request.POST.get('code')
        session_code = request.session.get('verification_code')
        email = request.session.get('email')

        if input_code == session_code:
            # Código correcto → redirigir a cambio de contraseña
            return redirect('change_password')
        else:
            messages.error(request, 'Código incorrecto.')
            return redirect('verify_code')

    return render(request, 'recuperar/codigo_recuperacion.html')


def change_password(request):
    """Vista para cambiar la contraseña después de validar el código"""
    email = request.session.get('email')

    if not email:
        messages.error(request, 'Primero solicita un código de recuperación.')
        return redirect('send_verification_code')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('change_password')

        # Cambiar contraseña del usuario
        user = Usuario.objects.get(email=email)
        user.set_password(password)
        user.save()

        # Limpiar sesión
        del request.session['email']
        del request.session['verification_code']

        messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
        return redirect('login')

    return render(request, 'recuperar/cambiar_contraseña.html')



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
        
        
class PasswordView(TemplateView):
    template_name = 'recuperar/recuperar_contraseña.html'
    def home(request):
        return render(request, "recuperar_contraseña.html")





