# applications/cuestionario/views.py
from django.shortcuts import render
from applications.Apispoonacular.api_services import buscar_plan_de_comidas

def generador_dieta(request):
    plan_de_comidas = None
    
    # Valores de ejemplo (en tu proyecto real, estos vendrían de un formulario)
    calorias_objetivo = 5000 
    
    # Llama a la función del servicio
    plan_de_comidas = buscar_plan_de_comidas(calorias_objetivo)
    
    context = {
        'plan': plan_de_comidas,
        'calorias': calorias_objetivo
    }
    
    return render(request, 'Apispoonacular/dieta_generada.html', context)