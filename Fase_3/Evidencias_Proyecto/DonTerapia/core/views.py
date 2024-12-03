from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .models import Actividad, FeedbackActividad, FeedbackTarea, UsuarioPersonalizado, ActividadRealizada, TareaAsignada,RespuestaTarea
from django.http import HttpResponse


def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.es_terapeuta:
                    return redirect('terapeuta')
                elif user.es_paciente:
                    return redirect('paciente')
                else:
                    messages.error(request, 'No tienes permisos asignados.')
                    return redirect('login')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
                return redirect('login')
        else:
            messages.error(request, 'Formulario inválido.')
            return render(request, 'app/login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'app/login.html', {'form': form})


@login_required
def vista_terapeuta(request):
 
    return render(request, 'app/terapeuta.html')


@login_required
def vista_paciente(request):


    return render(request, 'app/paciente.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'app/home.html')


@login_required
def actividades_vista(request):
    actividades = Actividad.objects.all()  # Obtener todas las actividades predefinidas
    pacientes = UsuarioPersonalizado.objects.filter(es_paciente=True)
    return render(request, 'app/actividades.html', {'actividades': actividades, 'pacientes': pacientes})

@login_required
def asignar_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)

    # Solo permitir acceso si el usuario es terapeuta
    if request.user.es_terapeuta:
        # Obtener todos los pacientes disponibles para la asignación
        pacientes = UsuarioPersonalizado.objects.filter(es_paciente=True)

        if request.method == 'POST':
            # Obtener los IDs de los pacientes seleccionados desde el formulario
            pacientes_ids = request.POST.getlist('pacientes')
            if not pacientes_ids:
                messages.error(request, "No seleccionaste ningún paciente.")
                return render(request, 'app/actividades.html', {'actividad': actividad, 'pacientes': pacientes})

            for paciente_id in pacientes_ids:
                paciente = UsuarioPersonalizado.objects.get(id=paciente_id)

                # Verificar si la actividad ya está asignada al paciente
                if not paciente.actividades.filter(id=actividad.id).exists():
                    paciente.actividades.add(actividad)

                # Crear una tarea asignada si no existe ya una para esta actividad y paciente
                if not TareaAsignada.objects.filter(actividad=actividad, asignada_a=paciente).exists():
                    TareaAsignada.objects.create(
                        actividad=actividad,
                        asignada_a=paciente,
                        descripcion=f"Tarea para {actividad.titulo} asignada al paciente {paciente.username}"
                    )

            messages.success(request, 'Actividad y tareas asignadas correctamente.')
            return redirect('actividades')  # Cambia la redirección según la vista correcta en tu aplicación

        return render(request, 'app/actividades.html', {'actividad': actividad, 'pacientes': pacientes})

    else:
        messages.error(request, 'No tienes permisos para asignar actividades.')
        return redirect('login')


@login_required
def actividades_asignadas(request):
    paciente_actual = request.user

    # Obtener actividades asignadas al paciente que tengan tareas incompletas
    actividades_con_tareas_incompletas = Actividad.objects.filter(
        tareas_asignadas_a_usuarios__asignada_a=paciente_actual,
        tareas_asignadas_a_usuarios__completada=False
    ).distinct()

    # Obtener solo las tareas no completadas relacionadas con el paciente
    tareas_incompletas = TareaAsignada.objects.filter(asignada_a=paciente_actual, completada=False)

    return render(request, 'app/actividades_asignadas.html', {
        'actividades': actividades_con_tareas_incompletas,
        'tareas_asignadas': tareas_incompletas
    })

@login_required
def realizar_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)

    if request.user.es_paciente:  # Verifica que el usuario sea paciente
        actividad_realizada = False  # Variable para controlar el modal

        if actividad.titulo == "ANALISIS DE CONDUCTA (ACC)":  # Verifica si es la actividad 1
            if request.method == 'POST':
                antecedentes = request.POST.get('antecedentes')
                conducta = request.POST.get('conducta')
                consecuencia = request.POST.get('consecuencia')
                fecha_hora = request.POST.get('fecha_hora')

                # Guardar la actividad realizada en la base de datos
                actividad_realizada_obj = ActividadRealizada.objects.create(
                    paciente=request.user,
                    actividad=actividad,
                    antecedentes=antecedentes,
                    conducta=conducta,
                    consecuencia=consecuencia,
                    fecha_hora=fecha_hora
                )

                # Eliminar la actividad de las asignadas
                request.user.actividades.remove(actividad)

                # Marcar la actividad como completada
                actividad_realizada_obj.completada = True
                actividad_realizada_obj.save()

                # Indicar que la actividad se ha realizado
                actividad_realizada = True

            return render(request, 'app/realizar_actividad_acc.html', {
                'actividad': actividad,
                'actividad_realizada': actividad_realizada
            })
        else:
            if request.method == 'POST':
                respuesta = request.POST.get('respuesta')

                # Guardar la respuesta (puedes ajustarlo según lo que necesites)
                ActividadRealizada.objects.create(
                    paciente=request.user,
                    actividad=actividad,
                    respuesta=respuesta
                )

                # Eliminar la actividad de las asignadas
                request.user.actividades.remove(actividad)

                actividad_realizada = True

            return render(request, 'app/realizar_actividad.html', {
                'actividad': actividad,
                'actividad_realizada': actividad_realizada
            })
    else:
        messages.error(request, 'No tienes permisos para realizar esta actividad.')
        return redirect('login')


    
@login_required
def asignar_actividad_con_tareas(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    pacientes = UsuarioPersonalizado.objects.filter(es_paciente=True)  # Obtener solo los pacientes

    if request.method == 'POST':
        pacientes_ids = request.POST.getlist('pacientes')  # Obtener los IDs de los pacientes seleccionados
        tareas_descripciones = request.POST.getlist('tareas')  # Obtener la lista de tareas

        for paciente_id in pacientes_ids:
            paciente = UsuarioPersonalizado.objects.get(id=paciente_id)

            # Asignar la actividad solo al paciente seleccionado si no la tiene ya asignada
            if not paciente.actividades.filter(id=actividad.id).exists():
                paciente.actividades.add(actividad)
                paciente.save()

            # Asignar hasta 5 tareas nuevas que no hayan sido asignadas previamente
            for tarea_desc in tareas_descripciones[:5]:
                if tarea_desc.strip():  # Evitar tareas vacías
                    # Verificar si la tarea ya existe para este paciente y actividad
                    if not TareaAsignada.objects.filter(actividad=actividad, asignada_a=paciente, descripcion=tarea_desc).exists():
                        TareaAsignada.objects.create(
                            actividad=actividad,
                            asignada_a=paciente,
                            descripcion=tarea_desc
                        )

        # Cambiamos el redirect por el render con la variable de éxito
        return render(request, 'app/asignar_actividad_tareas.html', {
            'actividad': actividad,
            'pacientes': pacientes,
            'tareas_asignadas': True  # Variable que activa el modal de éxito
        })

    return render(request, 'app/asignar_actividad_tareas.html', {'actividad': actividad, 'pacientes': pacientes})


    # Obtener las tareas ya asignadas para excluirlas de la vista
    tareas_asignadas = TareaAsignada.objects.filter(actividad=actividad, asignada_a__in=pacientes)
    tareas_excluidas = tareas_asignadas.values_list('descripcion', flat=True)

    return render(request, 'app/asignar_actividad_tareas.html', {
        'actividad': actividad,
        'pacientes': pacientes,
        'tareas_excluidas': tareas_excluidas  # Excluir las tareas que ya están asignadas
    })



@login_required
def realizar_actividad_con_tareas(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)

    # Filtrar solo las tareas no completadas
    tareas = TareaAsignada.objects.filter(actividad=actividad, asignada_a=request.user, completada=False)

    if request.method == 'POST':
        for tarea in tareas:
            respuesta = request.POST.get(f'tarea_{tarea.id}')
            
            # Guardar la respuesta del paciente en la base de datos
            RespuestaTarea.objects.create(
                tarea=tarea,
                respuesta=respuesta
            )

        # Marcar las tareas como completadas
        TareaAsignada.objects.filter(actividad=actividad, asignada_a=request.user).update(completada=True)

        # Mostrar el modal de éxito y redirigir al listado de actividades asignadas
        return render(request, 'app/realizar_actividad_con_tareas.html', {
            'actividad': actividad,
            'tareas': tareas,
            'actividad_realizada': True
        })

    return render(request, 'app/realizar_actividad_con_tareas.html', {
        'actividad': actividad,
        'tareas': tareas,
        'actividad_realizada': False
    })



@login_required
def asignar_tareas(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)

    if request.method == 'POST':
        tareas = request.POST.getlist('tareas')
        pacientes_ids = request.POST.getlist('pacientes')

        for paciente_id in pacientes_ids:
            paciente = UsuarioPersonalizado.objects.get(id=paciente_id)
            for tarea in tareas:
                if tarea.strip():
                    TareaAsignada.objects.create(
                        actividad=actividad,
                        asignada_a=paciente,
                        descripcion=tarea
                    )

        return redirect('actividades')

    pacientes = UsuarioPersonalizado.objects.filter(es_paciente=True)
    return render(request, 'app/asignar_tareas.html', {
        'actividad': actividad,
        'pacientes': pacientes
    })

@login_required
def ver_respuestas_tareas(request, paciente_id, actividad_id):
    paciente = get_object_or_404(UsuarioPersonalizado, id=paciente_id)
    actividad = get_object_or_404(Actividad, id=actividad_id)
    tareas = TareaAsignada.objects.filter(actividad=actividad, asignada_a=paciente)

    return render(request, 'app/ver_respuestas_tareas.html', {
        'paciente': paciente,
        'actividad': actividad,
        'tareas': tareas
    })

@login_required
def progreso_pacientes(request):
    if request.user.es_terapeuta:
        pacientes = UsuarioPersonalizado.objects.filter(es_paciente=True)
        return render(request, 'app/progreso_pacientes.html', {'pacientes': pacientes})
    else:
        messages.error(request, 'No tienes permisos para ver esta página.')
        return redirect('login')
    
@login_required
def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(UsuarioPersonalizado, id=paciente_id)

    if request.method == 'POST':
        paciente.first_name = request.POST.get('first_name', 'Nombre por defecto')  # Asigna un nombre por defecto si está vacío
        paciente.last_name = request.POST.get('last_name', '')
        paciente.email = request.POST.get('email', '')

        paciente.save()
        messages.success(request, 'Paciente actualizado correctamente.')
        return redirect('progreso_pacientes')
    
    return render(request, 'app/editar_paciente.html', {'paciente': paciente})

@login_required
def ver_actividades_paciente(request, paciente_id):
    paciente = get_object_or_404(UsuarioPersonalizado, id=paciente_id)
    
    # Obtener actividades realizadas por el paciente
    actividades_realizadas = ActividadRealizada.objects.filter(paciente=paciente)
    
    # Obtener respuestas de las tareas asignadas para la actividad 2 y demás
    respuestas_tareas = RespuestaTarea.objects.filter(tarea__asignada_a=paciente)

    return render(request, 'app/ver_actividades_paciente.html', {
        'paciente': paciente,
        'actividades_realizadas': actividades_realizadas,
        'respuestas_tareas': respuestas_tareas
    })

@login_required
def ver_actividades_reflexion_diaria(request, paciente_id):
    paciente = get_object_or_404(UsuarioPersonalizado, id=paciente_id)
    
    # Obtener la actividad "Reflexión diaria"
    actividad_reflexion = Actividad.objects.get(titulo="Reflexión diaria: ¿Cómo estuvo tu día?")
    
    # Obtener las respuestas del paciente para esta actividad
    respuestas = RespuestaTarea.objects.filter(tarea__actividad=actividad_reflexion, tarea__asignada_a=paciente)

    return render(request, 'app/ver_actividades_reflexion_diaria.html', {
        'paciente': paciente,
        'actividad': actividad_reflexion,
        'respuestas': respuestas
    })

@login_required
def ver_respuestas_actividad(request, actividad_realizada_id):
    actividad_realizada = get_object_or_404(ActividadRealizada, id=actividad_realizada_id)
    respuestas = RespuestaTarea.objects.filter(tarea__actividad=actividad_realizada.actividad, tarea__asignada_a=actividad_realizada.paciente)
    
    return render(request, 'app/ver_respuestas_actividad.html', {
        'actividad_realizada': actividad_realizada,
        'respuestas': respuestas
    })

@login_required
def ver_respuestas_tarea(request, respuesta_tarea_id):
    # Obtener la respuesta de la tarea especificada
    respuesta_tarea = get_object_or_404(RespuestaTarea, id=respuesta_tarea_id)
    
    # Obtener la tarea y su descripción (pregunta)
    tarea = respuesta_tarea.tarea

    return render(request, 'app/ver_respuestas_tarea.html', {
        'respuesta_tarea': respuesta_tarea,
        'tarea': tarea,
    })

@login_required
def ver_respuestas_actividad_acc(request, actividad_realizada_id):
    # Obtener la actividad realizada especificada
    actividad_realizada = get_object_or_404(ActividadRealizada, id=actividad_realizada_id)
    
    return render(request, 'app/ver_respuestas_actividad_acc.html', {
        'actividad_realizada': actividad_realizada,
    })
@login_required
def realizar_feedback_acc(request, actividad_realizada_id):
    actividad_realizada = get_object_or_404(ActividadRealizada, id=actividad_realizada_id)

    if request.method == 'POST':
        comentario = request.POST.get('comentario')

        # Crear y guardar el feedback en la base de datos
        FeedbackActividad.objects.create(
            actividad_realizada=actividad_realizada,
            terapeuta=request.user,
            comentario=comentario
        )
        messages.success(request, 'Feedback enviado correctamente.')
        return redirect('ver_actividades_paciente', paciente_id=actividad_realizada.paciente.id)  # Redirige a la página de actividades del paciente

    return render(request, 'app/realizar_feedback.html', {
        'actividad_titulo': actividad_realizada.actividad.titulo,
        'antecedentes': actividad_realizada.antecedentes,
        'conducta': actividad_realizada.conducta,
        'consecuencia': actividad_realizada.consecuencia,
    })

@login_required
def realizar_feedback_tarea(request, respuesta_tarea_id):
    respuesta_tarea = get_object_or_404(RespuestaTarea, id=respuesta_tarea_id)

    if request.method == 'POST':
        comentario = request.POST.get('comentario')

        # Crear y guardar el feedback en la base de datos
        FeedbackTarea.objects.create(
            respuesta_tarea=respuesta_tarea,
            terapeuta=request.user,
            comentario=comentario
        )
        messages.success(request, 'Feedback enviado correctamente.')
        return redirect('ver_actividades_paciente', paciente_id=respuesta_tarea.tarea.asignada_a.id)  # Redirige a la página de actividades del paciente

    return render(request, 'app/realizar_feedback.html', {
        'tarea_descripcion': respuesta_tarea.tarea.descripcion,
        'respuesta': respuesta_tarea.respuesta,
    })


@login_required
def ver_feedbacks(request):
    feedbacks_actividad = FeedbackActividad.objects.filter(terapeuta=request.user)
    feedbacks_tarea = FeedbackTarea.objects.filter(terapeuta=request.user)
    return render(request, 'app/ver_feedbacks.html', {
        'feedbacks_actividad': feedbacks_actividad,
        'feedbacks_tarea': feedbacks_tarea
    })



