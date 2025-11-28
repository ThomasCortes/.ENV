from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, FormView,TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import RegistroForm,LoginForm
from django.contrib import messages
from .forms import LoginForm  
#NUEVAS IMPORTACIONES
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
#OTRO NUEVO
from django.contrib.auth.hashers import make_password
#MAS CLASES




def send_verification_code(request):
    """Vista para solicitar el correo y enviar el código de recuperación"""
    if request.method == 'POST':
        email = request.POST.get('email')

        # Verificar si el correo existe
        if not User.objects.filter(email=email).exists():
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
            f'¡Hola!\nTu código de recuperacion de contraseña es: {code}\n'
            'Este código expira en unos minutos, así que te aconsejamos usarlo pronto\n'
            'Gracias por confiar en nosotros 💚',
            settings.EMAIL_HOST_USER,  # Desde el correo configurado
            [email],                   # Destinatario
            fail_silently=False,
        )

        messages.success(request, 'Se esta enviando un código a tu correo electronico.')
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
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        # Limpiar sesión
        del request.session['email']
        del request.session['verification_code']

        messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
        return redirect('login')

    return render(request, 'recuperar/cambiar_contraseña.html')



# Create your views here.
class RegisterView(FormView):
    template_name = 'login/register.html'
    form_class = RegistroForm
    success_url = reverse_lazy('cuestionario')

    def form_valid(self, form):
        # Crear el usuario
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        messages.success(self.request, "¡Registro exitoso! Bienvenido a Nutriet.")
        
        # Login automático
        login(self.request, user, backend='applications.Usuarios.backends.CustomAuthBackend')

        return super().form_valid(form)

    def form_invalid(self, form):
        # Mostrar errores de Django en SweetAlert (corrección)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)  # ← CAMBIO AQUÍ
        
        return self.render_to_response(self.get_context_data(form=form))

# Define la ruta de tu backend personalizado (Asegúrate de que esta sea la correcta)
CUSTOM_BACKEND = 'applications.Usuarios.backends.CustomAuthBackend'

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login/login.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        email_ingresado = form.cleaned_data.get('email')
        password_ingresada = form.cleaned_data.get('password')

        user = None
        
        # 1. Buscamos el usuario por el correo electrónico
        try:
            # Intentamos obtener el usuario que coincida con el email
            user = User.objects.get(email=email_ingresado)
        except User.DoesNotExist:
            # Si no existe, 'user' se queda como None
            pass 

        # 2. Si el usuario existe, verificamos la contraseña
        # La función check_password() es la que verifica el hash de la contraseña.
        if user is not None and user.check_password(password_ingresada):
            # Si es correcta, iniciamos sesión
            login(self.request, user)
            return super().form_valid(form)

        # Usuario no encontrado O contraseña incorrecta
        messages.error(self.request, 'Correo o contraseña incorrectos.')
        return self.form_invalid(form)
    
    def form_invalid(self, form):
        # ... (Mantén tu implementación existente) ...
        return self.render_to_response(self.get_context_data(form=form))
        
        
class PasswordView(TemplateView):
    template_name = 'recuperar/recuperar_contraseña.html'
    def home(request):
        return render(request, "recuperar_contraseña.html")


#VENTANAS EMERGENTES DEL REGISTER
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)

        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = make_password(form.cleaned_data["password"])
            usuario.save()

            messages.success(request, "¡Registro exitoso! Ya puedes iniciar sesión.")
            return redirect("login")
        else:
            messages.error(request, "Hay errores en el formulario. Revisa los campos.")
    else:
        form = RegistroForm()

    return render(request, "usuarios/registro.html", {"form": form})