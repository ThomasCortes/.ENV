from django.db import models
from applications.Usuarios.models import Usuario

# Create your models here.

# cuestionario models
sexo_choices = [
    ('masculino', 'Masculino'),
    ('femenino', 'Femenino'),
]

class CaracteristicasFisicas(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso en kilogramos")
    altura = models.DecimalField(max_digits=4, decimal_places=2, help_text="Altura en metros (ej: 1.75)")
    imc = models.DecimalField(max_digits=4, decimal_places=2, editable=False)  # No editable ya que se calcula automáticamente
    condicion_fisica = models.CharField(max_length=100)
    enfermedades = models.TextField()
    alergias = models.TextField()
    sexo = models.CharField(max_length=10 , choices=sexo_choices)

    def calcular_imc(self):
        try:
            # IMC = peso / (altura)²
            return round(float(self.peso) / (float(self.altura) ** 2), 2)
        except (ValueError, ZeroDivisionError):
            return 0

    def save(self, *args, **kwargs):
        # Calcular IMC antes de guardar
        self.imc = self.calcular_imc()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Características físicas de {self.usuario.nombre} - IMC: {self.imc}"

    class Meta:
        verbose_name = "Características Físicas"
        verbose_name_plural = "Características Físicas"

class ActividadFisica(models.Model):
    Intensidad_Choices = [
        ('sedentario', 'Sedentario'),
        ('ligero', 'Ligero'),
        ('moderado', 'Moderado'),
        ('intenso', 'Intenso'),
    ]
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    intensidad = models.CharField(max_length=50, choices=Intensidad_Choices)
    duracion_sesiones= models.IntegerField()  # duración en minutos
    tipo_actividad= models.CharField(max_length=100)

    def __str__(self):
        return f"Actividad física de {self.usuario.nombre} - {self.get_intensidad_display()}"

    class Meta:
        verbose_name = "Actividad Física"
        verbose_name_plural = "Actividades Físicas"

class Metas(models.Model):
    objetivo_choices = [
        ('perder', 'Perder peso'),
        ('mantener', 'Mantener peso'),
        ('ganar', 'Ganar peso'),
    ]
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    objetivo_peso= models.CharField(max_length=10, choices=objetivo_choices)
    plazo_meses= models.IntegerField()  # plazo en meses
    peso_objetivo= models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Meta de {self.usuario.nombre}: {self.get_objetivo_peso_display()} - {self.peso_objetivo}kg en {self.plazo_meses} meses"

    class Meta:
        verbose_name = "Meta"
        verbose_name_plural = "Metas"

class FrecuenciaComidas(models.Model):
    Frecuencia_CHOICES = [
        ('desayuno', 'Desayuno'),
        ('almuerzo', 'Almuerzo'),
        ('cena', 'Cena'),
        ('snacks', 'Snacks'),
    ]
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    frecuencia = models.CharField(max_length=100)

    def __str__(self):
        # 🟢 CORRECCIÓN: Usar directamente el valor del campo 'frecuencia'
        return f"Comidas de {self.usuario.nombre} - {self.frecuencia}" 

    class Meta:
        verbose_name = "Frecuencia de Comida"
        verbose_name_plural = "Frecuencias de Comidas"

class RestriccionesDietarias(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    vegetarianismo = models.BooleanField(default=False)
    veganismo= models.BooleanField(default=False)
    restricciones_economicas= models.BooleanField(default=False)
    alergias_alimentarias= models.BooleanField(default=False)


    def __str__(self):
        restricciones = []
        if self.vegetarianismo:
            restricciones.append("Vegetariano")
        if self.veganismo:
            restricciones.append("Vegano")
        if self.restricciones_economicas:
            restricciones.append("Restricciones económicas")
        if self.alergias_alimentarias:
            restricciones.append("Alergias alimentarias")
        
        if not restricciones:
            return f"{self.usuario.nombre} - Sin restricciones dietarias"
            
        return f"{self.usuario.nombre} - {' | '.join(restricciones)}"

    class Meta:
        verbose_name = "Restricción Dietaria"
        verbose_name_plural = "Restricciones Dietarias"

class Alimento(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, blank=True)
    emoji = models.CharField(max_length=5, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.emoji or ''} {self.nombre}"

class PreferenciaAlimentaria(models.Model):

    PREFERENCIA_CHOICES = [
        ('like', '😋 Me gusta'),
        ('dislike', '😐 No me gusta'),
        ('allergy', '🚫 No puedo consumir'),
        ('restrict', '⚠️ Evitar por recomendación'),
    ]
    restriccion_relacionada = models.ForeignKey('RestriccionesDietarias', on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey('Usuarios.Usuario', on_delete=models.CASCADE)
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    preferencia = models.CharField(max_length=10, choices=PREFERENCIA_CHOICES)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.alimento.nombre}: {self.get_preferencia_display()}"

    class Meta:
        unique_together = ('usuario', 'alimento')


 #seguimiento de dieta
class AlimentosConsumidos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha= models.DateField(auto_now_add=True)
    consumo = models.BooleanField(default=False)
    numero_comidas_dia= models.IntegerField()
    snacks_dia= models.IntegerField()
    calorias_totales= models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.fecha} - {self.calorias_totales} cal"

    class Meta:
        verbose_name = "Alimento Consumido"
        verbose_name_plural = "Alimentos Consumidos"

#alimentos 

class Recetas(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    nombre_receta= models.CharField(max_length=100)
    ingredientes= models.TextField()
    instrucciones= models.TextField()
    calorias= models.IntegerField()
    proteinas= models.DecimalField(max_digits=5, decimal_places=2)
    carbohidratos= models.DecimalField(max_digits=5, decimal_places=2)
    grasas= models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.nombre_receta} - {self.calorias} cal"

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"

