from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, redirect
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from notifications.models import Notification
from notifications.signals import notify

from InclusionEducativa.Apps.AppExperto.models import Comentario, ExpertoFichaInformativa
from InclusionEducativa.Apps.AppRepresentante.models import *
from InclusionEducativa.Apps.AppDocente.models import *
from InclusionEducativa.Apps.GestionSistema.models import *
from InclusionEducativa.Apps.GestionSistema.forms import *

notificaciones = None


def perfil(request):
    usuario_logueado = request.user
    usuario = Usuario.objects.get(id=request.user.id)
    form_usuario = UsuarioForm(request.POST, instance=usuario)
    if request.method == 'POST':
        if form_usuario.is_valid():
            form_usuario.save()

        return redirect('gestionsistema:base')
    return render(request, 'AppExperto/perfil.html', {'usuario': usuario,
                                                      'usuario_logueado': usuario_logueado})


def base(request):
    usuario_logueado = request.user
    experto = Experto.objects.get(usuario_id=request.user.id)
    estudiantes = []
    if ExpertoFichaInformativa.objects.filter(experto_id=experto.id).exists():
        expertoFichasInformativas = ExpertoFichaInformativa.objects.filter(experto_id=experto.id)
        for expertoFichaInformativa in expertoFichasInformativas:
            if expertoFichaInformativa.fichaInformativaDocente and expertoFichaInformativa.fichaInformativaRepresentante:
                estudiantes.append(
                    Estudiante.objects.get(cedula=expertoFichaInformativa.fichaInformativaDocente.estudiante.cedula))
            elif expertoFichaInformativa.fichaInformativaDocente and not expertoFichaInformativa.fichaInformativaRepresentante:
                estudiantes.append(
                    Estudiante.objects.get(cedula=expertoFichaInformativa.fichaInformativaDocente.estudiante.cedula))
            elif not expertoFichaInformativa.fichaInformativaDocente and expertoFichaInformativa.fichaInformativaRepresentante:
                estudiantes.append(
                    Estudiante.objects.get(
                        cedula=expertoFichaInformativa.fichaInformativaRepresentante.estudiante.cedula))
    return render(request, 'AppExperto/base.html',
                  {'estudiantes': estudiantes,
                   'usuario_logueado': usuario_logueado
                   })


@login_required
def onesignal_register(request):
    experto = Experto.objects.get(user=request.user)  # The model where you will to save the profile.
    if request.POST.get('playerId'):
        experto.onesignal_playerId = request.POST.get('playerId')
        experto.save()
        return HttpResponse('Done')
    return HttpResponse('Something went wrong')


def verFicha(request, cedula):
    usuario_logueado = request.user
    estudiante = Estudiante.objects.get(cedula=cedula)
    if Notification.objects.filter(target_object_id=estudiante.id).exists():
        notificaciones = Notification.objects.filter(target_object_id=estudiante.id)
        for notificacion in notificaciones:
            notificacion.mark_as_read()
    if FichaInformativaDocente.objects.filter(estudiante_id=estudiante.id).exists():
        fichaInformativaDocente = FichaInformativaDocente.objects.get(estudiante_id=estudiante.id)
    else:
        fichaInformativaDocente = None
    if FichaInformativaRepresentante.objects.filter(estudiante_id=estudiante.id).exists():
        fichaInformativaRepresentante = FichaInformativaRepresentante.objects.get(estudiante_id=estudiante.id)
    else:
        fichaInformativaRepresentante = None
    return render(request, 'AppExperto/verFichaInformativa.html',
                  {'estudiante': estudiante,
                   'fichaInformativaDocente': fichaInformativaDocente,
                   'fichaInformativaRepresentante': fichaInformativaRepresentante,
                   'usuario_logueado': usuario_logueado})


@csrf_exempt
def crearComentario(request):
    if request.method == 'POST':
        comentario = Comentario()
        comentario.contenido = request.POST['contenidoComentario']
        comentario.emisor = request.user
        estudiante = Estudiante.objects.get(id=request.POST['id'])
        comentario.estudiante = estudiante
        comentario.usernameEmisor = request.user.username
        comentario.save()
        receptores = []
        representante = FichaInformativaRepresentante.objects.get(estudiante_id=estudiante.id).representante.usuario
        receptores.append(representante)
        docente = FichaInformativaDocente.objects.get(estudiante_id=estudiante.id).docente.usuario
        receptores.append(docente)
        verbDocente = "/appdocente/verFichaInformativa/" + estudiante.cedula
        descripcion = "Nuevo comentario de " + request.user.nombres
        verbRepresente = "apprepresentante/verFichaInformativa/" + estudiante.cedula
        notify.send(request.user, recipient=docente, actor=request.user,
                    verb=verbDocente,
                    description=descripcion, target=estudiante)
        notify.send(request.user, recipient=representante, actor=request.user,
                    verb=verbRepresente + estudiante.cedula,
                    description=descripcion, target=estudiante)
