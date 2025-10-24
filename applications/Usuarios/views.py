from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegistroForm,LoginForm

# Create your views here.

class RegisterView(CreateView):
    form_class =RegistroForm
    template_name ='login/register.html'
    success_url = reverse_lazy('login')

class LoginView(CreateView):
    form_class = LoginForm
    template_name = 'login/login.html'
    success_url =reverse_lazy ('home/index.html')