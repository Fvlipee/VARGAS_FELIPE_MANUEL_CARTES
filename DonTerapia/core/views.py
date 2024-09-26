from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)  # Ajustado para usar correctamente la instancia del formulario
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirigir según el rol del usuario
                if user.terapeuta:  # Simplificado sin usar hasattr
                    return redirect('terapeuta')  # Asume que tienes una URL nombrada 'terapeuta'
                elif user.paciente:  # Simplificado sin usar hasattr
                    return redirect('paciente')  # Asume que tienes una URL nombrada 'paciente'
                else:
                    messages.error(request, 'No tienes permisos asignados.')
                    return redirect('login')  # Redirige de nuevo a login si no tiene roles
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
                return redirect('login')  # Redirige de nuevo a login si la autenticación falla
        else:
            messages.error(request, 'Formulario inválido')
            return render(request, 'app/login.html', {'form': form})  # Vuelve a renderizar la página de login con errores
    else:
        form = LoginForm()

    return render(request, 'app/login.html', {'form': form})

@login_required
def vista_terapeuta(request):
    return render(request, 'app/terapeuta.html')  # Usar la ruta completa

@login_required
def vista_paciente(request):
    return render(request, 'app/paciente.html')  # Usar la ruta completa

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'app/home.html')

def actividades_view(request):
    # Asumiendo que tienes una lógica para obtener las actividades o algo similar
    return render(request, 'app/actividades.html')

