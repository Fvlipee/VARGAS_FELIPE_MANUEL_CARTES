from django.urls import path
from .views import home, iniciar_sesion, user_logout, vista_terapeuta, vista_paciente,actividades_view



urlpatterns = [
    path('', home, name='home'),
    path('login/', iniciar_sesion, name='login'),
    path('logout/', user_logout, name='logout'),
    path('terapeuta/', vista_terapeuta, name='terapeuta'),
    path('paciente/', vista_paciente, name='paciente'),
    path('actividades/', actividades_view, name='actividades'),
]
