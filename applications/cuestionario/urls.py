from applications.cuestionario.views import cuestionario_completado
from django.urls import path, include
from applications.cuestionario.views import CuestionarioWizard, FORMS
from django.shortcuts import render

urlpatterns = [
    path('cuestionario/', CuestionarioWizard.as_view(FORMS), name='cuestionario'),
     path('cuestionario/completado/', cuestionario_completado, name='cuestionario_completado'),
]