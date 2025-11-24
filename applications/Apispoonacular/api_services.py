# applications/external/api_services.py
import requests
from django.conf import settings

def buscar_plan_de_comidas(target_calories, diet=None, exclusions=None):
    """
    Busca un plan de comidas diario utilizando la API de Spoonacular.
    Documentación: https://spoonacular.com/api/docs/
    """
    url = settings.SPOONACULAR_BASE_URL + 'mealplanner/generate'
    params = {
        'apiKey': settings.SPOONACULAR_API_KEY,
        'timeFrame': 'day', # Para un plan de un día
        'targetCalories': target_calories,
    }
    
    if diet:
        params['diet'] = diet # Ej: 'vegetarian', 'vegan'
    if exclusions:
        params['exclude'] = exclusions # Ej: 'peanuts', 'shellfish'

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Lanza HTTPError si la respuesta fue un error
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al consumir la API de Spoonacular: {e}")
        return None 