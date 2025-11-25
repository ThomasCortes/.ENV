from django.db import models

class Actividad(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.fecha})"
