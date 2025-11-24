from django import forms

from applications.base.models import (
    CaracteristicasFisicas,
    ActividadFisica,
    Metas,
    FrecuenciaComidas,
    RestriccionesDietarias,
    Alimento,
    PreferenciaAlimentaria
)

# --------------------------
# 1️⃣ Formulario Características Físicas
# --------------------------
class CaracteristicasFisicasForm(forms.ModelForm):
    class Meta:
        model = CaracteristicasFisicas
        fields = ['peso', 'altura', 'condicion_fisica', 'enfermedades', 'alergias', 'sexo']
        widgets = {
            'sexo': forms.RadioSelect(choices=[
                ('masculino', 'Masculino'),
                ('femenino', 'Femenino')
            ]),
            'condicion_fisica': forms.TextInput(attrs={'placeholder': 'Ej: Buena, Regular, Mala'}),
            'enfermedades': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ej: Hipertensión, diabetes...'}),
            'alergias': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ej: Gluten, maní...'}),
        }


# --------------------------
# 2️⃣ Formulario Actividad Física
# --------------------------
class ActividadFisicaForm(forms.ModelForm):
    class Meta:
        model = ActividadFisica
        fields = ['intensidad', 'duracion_sesiones', 'tipo_actividad']
        widgets = {
            'intensidad': forms.RadioSelect(choices=[
                ('sedentario', 'Sedentario'),
                ('ligero', 'Ligero'),
                ('moderado', 'Moderado'),
                ('intenso', 'Intenso')
            ]),
            'duracion_sesiones': forms.NumberInput(attrs={'placeholder': 'Duración promedio en minutos'}),
            'tipo_actividad': forms.TextInput(attrs={'placeholder': 'Ej: Correr, Gimnasio, Caminar...'}),
        }


# --------------------------
# 3️⃣ Formulario Metas
# --------------------------
class MetasForm(forms.ModelForm):
    class Meta:
        model = Metas
        fields = ['objetivo_peso', 'plazo_meses', 'peso_objetivo']
        widgets = {
            'objetivo_peso': forms.RadioSelect(choices=[
                ('perder', 'Perder peso'),
                ('mantener', 'Mantener peso'),
                ('ganar', 'Ganar peso')
            ]),
            'plazo_meses': forms.NumberInput(attrs={'placeholder': 'Ej: 3'}),
            'peso_objetivo': forms.NumberInput(attrs={'placeholder': 'Ej: 65.0'}),
        }


# --------------------------
# 4️⃣ Formulario Restricciones Dietarias
# --------------------------
class RestriccionesDietariasForm(forms.ModelForm):
    class Meta:
        model = RestriccionesDietarias
        fields = ['vegetarianismo', 'veganismo', 'restricciones_economicas', 'alergias_alimentarias']
        widgets = {
            'vegetarianismo': forms.CheckboxInput(),
            'veganismo': forms.CheckboxInput(),
            'restricciones_economicas': forms.CheckboxInput(),
            'alergias_alimentarias': forms.CheckboxInput(),
        }


# --------------------------
# 5️⃣ Formulario Preferencias Alimentarias (Panel de Emojis 🍎🍗🥦)
# --------------------------
class PreferenciaAlimentariaForm(forms.Form):
    """
    Este formulario se genera dinámicamente a partir de los alimentos registrados.
    El usuario elige una preferencia por cada alimento: 😋 / 😐 / 🚫
    """
    PREFERENCIA_CHOICES = [
        ('like', '😋 Me gusta'),
        ('dislike', '😐 No me gusta'),
        ('allergy', '🚫 No puedo consumir'),
    ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Recibir usuario opcional
        super().__init__(*args, **kwargs)

        alimentos = Alimento.objects.all().order_by('categoria', 'nombre')

        for alimento in alimentos:
            field_name = f"alimento_{alimento.id}"
            label = f"{alimento.emoji or ''} {alimento.nombre}"
            self.fields[field_name] = forms.ChoiceField(
                label=label,
                choices=self.PREFERENCIA_CHOICES,
                widget=forms.RadioSelect(attrs={'class': 'emoji-choice'}),
                required=False
            )

    def save(self, usuario):
        """
        Guarda todas las preferencias seleccionadas.
        """
        for field_name, value in self.cleaned_data.items():
            if not value:
                continue
            alimento_id = field_name.split('_')[1]
            PreferenciaAlimentaria.objects.update_or_create(
                usuario=usuario,
                alimento_id=alimento_id,
                defaults={'preferencia': value}
            )

class FrecuenciaComidasForm(forms.ModelForm):
    Frecuencia_CHOICES = [
        ('desayuno', 'Desayuno'),
        ('almuerzo', 'Almuerzo'),
        ('cena', 'Cena'),
        ('snacks', 'Snacks'),
    ]

    frecuencia = forms.MultipleChoiceField(
        choices=FrecuenciaComidas.Frecuencia_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="¿Cuáles comidas realizas al día?"
    )

    class Meta:
        model = FrecuenciaComidas
        fields = ['frecuencia']