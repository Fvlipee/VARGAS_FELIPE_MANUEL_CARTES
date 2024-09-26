from django.contrib.auth.models import AbstractUser
from django.db import models

class UsuarioPersonalizado(AbstractUser):
    terapeuta = models.BooleanField(default=False)
    paciente = models.BooleanField(default=False)
