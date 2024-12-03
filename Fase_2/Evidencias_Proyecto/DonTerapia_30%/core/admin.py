from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado

@admin.register(UsuarioPersonalizado)
class UsuarioPersonalizadoAdmin(UserAdmin):
    model = UsuarioPersonalizado
    fieldsets = (
        *UserAdmin.fieldsets,  # Default fieldsets
        ('Extra State', {'fields': ('terapeuta', 'paciente',)}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'terapeuta', 'paciente', 'is_staff']
    list_filter = ['terapeuta', 'paciente', 'is_staff', 'is_superuser', 'is_active']
