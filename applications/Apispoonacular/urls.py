# applications/cuestionario/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... otras URLs
    path('generar-dieta/', views.generador_dieta, name='generar_dieta'),
]