from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .formas import TareaForm
from .models import Tarea
from django.utils import timezone


def v_paginainicio(request):
    return render(request, 'paginainicio.html')


def v_paginaregistro(request):
    if request.method == 'GET':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tareas')

    return render(request, 'paginaregistro.html', {'form': form})


@login_required
def tareas(request):
    tareas = Tarea.objects.filter(usuario=request.user, dato_completo__isnull=True)
    return render(request, 'tareas.html', {'tareas': tareas, 'tipopagina': 'Tareas Pendientes'})


@login_required
def crear_tarea(request):
    if request.method == 'GET':
        form = TareaForm()
    else:
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = request.user
            tarea.save()
            return redirect('tareas')

    return render(request, 'crear_tarea.html', {'form': form})

@login_required
def tareas_completadas(request):
    tareas = Tarea.objects.filter(usuario=request.user, dato_completo__isnull=False).order_by('-dato_completo')
    return render(request, 'tareas.html', {'tareas': tareas, 'tipopagina': 'Tareas Completadas'})

@login_required
def tarea_completa(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.dato_completo = timezone.now()
        tarea.save()
        return redirect('tareas')
    return redirect('detalle_tarea', tarea_id=tarea.id)


@login_required
def tarea_eliminar(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tareas')
    return redirect('detalle_tarea', tarea_id=tarea.id)


@login_required
def tarea_detalle(request, tarea_id): ###task_detail
    tarea = get_object_or_404(Tarea, pk=tarea_id, usuario=request.user)
    if request.method == 'GET':
        form = TareaForm(instance=tarea)
    else:
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('tareas')

    return render(request, 'detalle_tarea.html', {
        'tarea': tarea,
        'form': form,
    })


def v_paginacerrar(request): ###logout
    logout(request)
    return redirect('paginainicial')


def v_iniciarsesion(request): ###signin
    if request.method == 'GET':
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(request, data=request.POST)
        user = form.get_user() if form.is_valid() else None
        if user is None:
            error = 'El nombre de usuario o la contraseña son incorrectos'
        else:
            login(request, user)
            return redirect('tareas')

        return render(request, 'iniciarsesion.html', {
            'form': form,
            'error': error,
        })

    return render(request, 'iniciarsesion.html', {'form': form})

