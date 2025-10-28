from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, password=None):
        if not email:
            raise ValueError('Los usuarios deben tener un correo electrónico válido')

        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, password=None):
        user = self.create_user(email, nombre, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):  # 👈 Agrega PermissionsMixin aquí
    nombre = models.CharField('Nombre completo', max_length=150, unique=True)
    email = models.EmailField('Correo electrónico', unique=True)
    password = models.CharField('Contraseña', max_length=128)
    numero_telefono = models.CharField('Número de teléfono', max_length=15, blank=True, null=True)

    date_joined = models.DateTimeField('Fecha de registro', auto_now_add=True)
    last_login = models.DateTimeField('Último inicio de sesión', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.nombre
