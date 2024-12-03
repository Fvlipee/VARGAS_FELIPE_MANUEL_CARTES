from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

# Modelo de usuario personalizado
class UsuarioPersonalizado(AbstractUser):
    es_terapeuta = models.BooleanField(default=False)
    es_paciente  = models.BooleanField(default=False)
    actividades = models.ManyToManyField('Actividad', blank=True)  # Relación ManyToMany con Actividad
    tareas = models.ManyToManyField('Tarea', blank=True)
    
    def __str__(self):
        return self.username

# Modelo de actividad
class Actividad(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen_url = models.CharField(max_length=255, null=True, blank=True)  # Para permitir URL vacías o nulas

    def __str__(self):
        return self.titulo

# Modelo de tarea asignada
class Tarea(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='tareas')
    asignada_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tareas_asignadas')
    descripcion = models.TextField()
    completada = models.BooleanField(default=False)  # Para marcar si la tarea está completada

    def __str__(self):
        return f"Tarea para {self.asignada_a.username} - {self.descripcion}"

class TareaAsignada(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='tareas_asignadas_a_usuarios')
    asignada_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completada = models.BooleanField(default=False)  # Campo para indicar si la tarea fue completada
    descripcion = models.TextField()

    def __str__(self):
        return f"Tarea para {self.asignada_a.username} - {self.descripcion}"
    
# Modelo para registrar la respuesta del paciente a la tarea
class RespuestaTarea(models.Model):
    tarea = models.ForeignKey(TareaAsignada, on_delete=models.CASCADE, related_name='respuestas')
    respuesta = models.TextField()
    fecha_realizacion = models.DateTimeField(auto_now_add=True)  # Fecha en que se registró la actividad

    def __str__(self):
        return f"Respuesta a la tarea: {self.tarea.descripcion}"

class ActividadRealizada(models.Model):
    paciente = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Relacionado al paciente que realizó la actividad
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)  # Relacionado a la actividad
    antecedentes = models.TextField(default="Sin antecedentes")
    conducta = models.TextField(default="Sin conducta")
    consecuencia = models.TextField(default="Sin consecuencia")
    fecha_hora = models.DateTimeField()  # Fecha y hora del suceso
    fecha_realizacion = models.DateTimeField(auto_now_add=True)  # Fecha en que se registró la actividad

    def __str__(self):
        return f"Actividad realizada por {self.paciente.username} - {self.actividad.titulo}"
    
class FeedbackActividad(models.Model):
    actividad_realizada = models.ForeignKey('ActividadRealizada', on_delete=models.CASCADE, related_name='feedback_actividad')
    terapeuta = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback de {self.terapeuta.username} para {self.actividad_realizada.actividad.titulo}"

class FeedbackTarea(models.Model):
    respuesta_tarea = models.ForeignKey('RespuestaTarea', on_delete=models.CASCADE, related_name='feedback_tarea')
    terapeuta = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback de {self.terapeuta.username} para {self.respuesta_tarea.tarea.descripcion}"

