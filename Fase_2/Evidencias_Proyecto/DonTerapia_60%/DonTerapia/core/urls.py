from django.urls import path
from .views import home, iniciar_sesion, user_logout, vista_terapeuta, vista_paciente,actividades_vista,asignar_actividad,actividades_asignadas,realizar_actividad,ver_respuestas_tareas,asignar_tareas,realizar_actividad_con_tareas,progreso_pacientes,editar_paciente,ver_actividades_paciente,ver_actividades_reflexion_diaria,ver_respuestas_actividad,realizar_feedback_acc,ver_respuestas_tarea,realizar_feedback_tarea,ver_respuestas_actividad_acc


urlpatterns = [
    path('', home, name='home'),
    path('login/', iniciar_sesion, name='login'),
    path('logout/', user_logout, name='logout'),
    path('terapeuta/', vista_terapeuta, name='terapeuta'),
    path('paciente/', vista_paciente, name='paciente'),
    path('actividades/', actividades_vista, name='actividades'),
    path('asignar_actividad/<int:actividad_id>/', asignar_actividad, name='asignar_actividad'),
    path('actividades_asignadas/', actividades_asignadas, name='actividades_asignadas'),
    path('realizar_actividad/<int:actividad_id>/', realizar_actividad, name='realizar_actividad'),
    path('ver_respuestas_tareas/<int:paciente_id>/<int:actividad_id>/', ver_respuestas_tareas, name='ver_respuestas_tareas'),
    path('asignar_tareas/<int:actividad_id>/', asignar_tareas, name='asignar_tareas'),
    path('realizar_actividad_con_tareas/<int:actividad_id>/', realizar_actividad_con_tareas, name='realizar_actividad_con_tareas'),
    path('progreso_pacientes/', progreso_pacientes, name='progreso_pacientes'),
    path('editar_paciente/<int:paciente_id>/', editar_paciente, name='editar_paciente'),
    path('paciente/<int:paciente_id>/actividades/', ver_actividades_paciente, name='ver_actividades_paciente'),
    path('ver_actividades_reflexion_diaria/<int:paciente_id>/', ver_actividades_reflexion_diaria, name='ver_actividades_reflexion_diaria'),
    path('actividad/<int:actividad_realizada_id>/ver_respuestas/', ver_respuestas_actividad, name='ver_respuestas_actividad'),
    path('tarea/<int:respuesta_tarea_id>/ver_respuestas/', ver_respuestas_tarea, name='ver_respuestas_tarea'),
    path('actividad_acc/<int:actividad_realizada_id>/ver_respuestas/', ver_respuestas_actividad_acc, name='ver_respuestas_actividad_acc'),
    path('tarea/<int:respuesta_tarea_id>/realizar_feedback/', realizar_feedback_tarea, name='realizar_feedback_tarea'),
    path('actividad_acc/<int:actividad_realizada_id>/realizar_feedback/', realizar_feedback_acc, name='realizar_feedback_acc'),
]


