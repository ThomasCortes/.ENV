from django.shortcuts import render, redirect
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from formtools.wizard.views import SessionWizardView

from .forms import (
    CaracteristicasFisicasForm,
    ActividadFisicaForm,
    MetasForm,
    RestriccionesDietariasForm,
    PreferenciaAlimentariaForm,
    FrecuenciaComidasForm
)

from applications.base.models import (
    CaracteristicasFisicas,
    ActividadFisica,
    Metas,
    FrecuenciaComidas,
    RestriccionesDietarias,
)

FORMS = [
    ("caracteristicas", CaracteristicasFisicasForm),
    ("actividad", ActividadFisicaForm),
    ("metas", MetasForm),
    ("restricciones", RestriccionesDietariasForm),
    ("preferencias", PreferenciaAlimentariaForm),
    ("frecuencia", FrecuenciaComidasForm),
]

TEMPLATES = {
    "caracteristicas": "cuestionario/caracteristicas.html",
    "actividad": "cuestionario/actividad.html",
    "metas": "cuestionario/metas.html",
    "restricciones": "cuestionario/restricciones.html",
    "preferencias": "cuestionario/preferencias.html",
    "frecuencia": "cuestionario/frecuencia.html",
}


class CuestionarioWizard(LoginRequiredMixin, SessionWizardView):
    form_list = FORMS
    template_name = "cuestionario/base.html"
    login_url = '/login/'

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def render_next_step(self, form, **kwargs):
        if isinstance(form, FrecuenciaComidasForm) and form.is_valid():

            comidas = form.cleaned_data.get('comidas_seleccionadas')
            usuario = self.request.user

            FrecuenciaComidas.objects.filter(usuario=usuario).delete()

            if comidas:
                FrecuenciaComidas.objects.bulk_create([
                    FrecuenciaComidas(usuario=usuario, frecuencia=c)
                    for c in comidas
                ])

            self.storage.set_step_data(self.steps.current, form.data)

        return super().render_next_step(form, **kwargs)
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == "preferencias":

            api_key = settings.SPOONACULAR_API_KEY
            if not api_key:
                print("🔥 ERROR: No hay API KEY en settings.py")
                context["ingredientes_spoonacular"] = []
                return context

            try:
                url = "https://api.spoonacular.com/food/ingredients/search"
                params = {
                    "query": "fruit",      # <--- trae imágenes REALES
                    "number": 30,
                    "apiKey": api_key
                }

                res = requests.get(url, params=params)
                data = res.json()
                print("API RESPONSE:", data)

                ingredientes = []
                for item in data.get("results", []):
                    imagen = item.get("image", "")

                    # VALIDAR IMAGEN REAL
                    if imagen and not imagen.endswith("png") and not imagen.endswith("jpg"):
                        continue

                    ingredientes.append({
                        "id": item["id"],
                        "nombre": item["name"].capitalize(),
                        "imagen": f"https://spoonacular.com/cdn/ingredients_100x100/{imagen}"
                    })

                context["ingredientes_spoonacular"] = ingredientes

            except Exception as e:
                print("🔥 ERROR CON SPOONACULAR:", e)
                context["ingredientes_spoonacular"] = []

        return context

    def done(self, form_list, **kwargs):
        usuario = self.request.user

        for form in form_list:
            data = form.cleaned_data

            if isinstance(form, CaracteristicasFisicasForm):
                CaracteristicasFisicas.objects.update_or_create(
                    usuario=usuario, defaults=data
                )

            elif isinstance(form, ActividadFisicaForm):
                ActividadFisica.objects.update_or_create(
                    usuario=usuario, defaults=data
                )

            elif isinstance(form, MetasForm):
                Metas.objects.update_or_create(
                    usuario=usuario, defaults=data
                )

            elif isinstance(form, RestriccionesDietariasForm):
                RestriccionesDietarias.objects.update_or_create(
                    usuario=usuario, defaults=data
                )

            elif isinstance(form, PreferenciaAlimentariaForm):
                form.save(usuario)

        return redirect('cuestionario_completado')


@login_required(login_url='/login/')
def cuestionario_completado(request):
    return render(request, 'cuestionario/completado.html')
