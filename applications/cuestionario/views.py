from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  # 👈 Agregado
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


# -----------------------------
# 🧩 Lista de formularios y plantillas
# -----------------------------
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


# -----------------------------
# 🧠 Wizard principal
# -----------------------------
class CuestionarioWizard(LoginRequiredMixin, SessionWizardView):
    form_list = FORMS
    template_name = "cuestionario/base.html"
    login_url = '/login/'

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    # 🟢 NUEVO MÉTODO: Maneja la lógica de selección múltiple al avanzar de paso
    def render_next_step(self, form, **kwargs):
        if isinstance(form, FrecuenciaComidasForm) and form.is_valid():
            # Asumiendo que el campo en tu form.py se llama 'comidas_seleccionadas'
            comidas_seleccionadas = form.cleaned_data.get('comidas_seleccionadas')
            usuario = self.request.user
            
            # Borrar entradas antiguas y crear una nueva por cada selección
            FrecuenciaComidas.objects.filter(usuario=usuario).delete()
            
            if comidas_seleccionadas:
                objetos_a_crear = [
                    FrecuenciaComidas(usuario=usuario, frecuencia=comida) 
                    for comida in comidas_seleccionadas
                ]
                FrecuenciaComidas.objects.bulk_create(objetos_a_crear)

            # Guardar la data para que el Wizard sepa que el paso fue completado
            self.storage.set_step_data(self.steps.current, form.data)
            
        return super().render_next_step(form, **kwargs)


    def done(self, form_list, **kwargs):
        """Guarda todos los formularios cuando el usuario termina"""
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

            elif isinstance(form, FrecuenciaComidasForm):
                # ❌ ELIMINADO: La lógica de guardado ya se manejó en render_next_step()
                #    Esta parte no debe hacer nada para FrecuenciaComidas.
                pass 
                
        return redirect('cuestionario_completado')  

@login_required(login_url='/login/')
def cuestionario_completado(request):
    """Muestra la página de confirmación al finalizar el cuestionario"""
    return render(request, 'cuestionario/completado.html')
