from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Custom user model used by the project.
    Se agregan los campos requeridos por las forms y modelos del proyecto:
    - nombre: para mantener compatibilidad con los templates/str del proyecto
    - telefono: utilizado por el formulario de registro
    """
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        # Mantener un nombre legible; si no hay nombre, usar el username
        return self.username