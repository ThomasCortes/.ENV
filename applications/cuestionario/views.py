from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
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
class CuestionarioWizard(SessionWizardView):
    form_list = FORMS
    template_name = "cuestionario/base.html"

    def get_template_names(self):
        """Selecciona la plantilla correspondiente al paso actual"""
        return [TEMPLATES[self.steps.current]]

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

            elif frecuencia_data and 'frecuencia' in frecuencia_data:
                frecuencia_data = self.get_cleaned_data_for_step('frecuencia_step_name')

                if frecuencia_data and 'frecuencia' in frecuencia_data:
                    frecuencia_data['frecuencia'] = ','.join(frecuencia_data['frecuencia'])
                    FrecuenciaComidas.objects.update_or_create(
                     usuario=usuario,
                    defaults=frecuencia_data
                )

            elif isinstance(form, PreferenciaAlimentariaForm):
                form.save(usuario)

        # ✅ Redirigir al completado
        return redirect('cuestionario_completado')


# -----------------------------
# ✅ Vista final de completado
# -----------------------------
@login_required
def cuestionario_completado(request):
    """Muestra la página de confirmación al finalizar el cuestionario"""
    return render(request, 'cuestionario/completado.html')