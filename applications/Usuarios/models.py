from django.db import models


# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField('Nombre completo', max_length=150, unique=True, blank=False)
    email = models.EmailField('Correo electrónico', unique=True, blank=False)
    password = models.CharField('Contraseña', max_length=128, blank=False)
    numero_telefono = models.CharField('Número de teléfono', max_length=15, blank=False)

    def __str__(self):
        return self.nombre
