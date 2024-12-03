from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado

@admin.register(UsuarioPersonalizado)
class UsuarioPersonalizadoAdmin(UserAdmin):
    model = UsuarioPersonalizado
    fieldsets = (
        *UserAdmin.fieldsets,  # Default fieldsets
        ('Extra State', {'fields': ('es_terapeuta', 'es_paciente',)}),  # Asegúrate de que uses los nombres correctos
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'es_terapeuta', 'es_paciente', 'is_staff']
    list_filter = ['es_terapeuta', 'es_paciente', 'is_staff', 'is_superuser', 'is_active']

# No es necesario registrar el modelo nuevamente, porque ya está registrado con el decorador
