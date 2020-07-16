from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.db import IntegrityError
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


@csrf_exempt
@login_required
def perfil(request, id_usuario):
    usuario_logueado = request.user
    usuario = Usuario.objects.get(id=request.user.id)
    if request.method == 'POST':
        try:
            usuario.nombres = request.POST['nombres']
            usuario.apellidos = request.POST['apellidos']
            usuario.username = request.POST['username']
            if bool(request.FILES.get('file', False)) == True:
                usuario.foto = request.FILES['file']
            usuario.email = usuario.username
            usuario.fechaNacimiento = request.POST['fechaNacimiento']
            usuario.save()
        except IntegrityError as e:
            messages.error(request, 'El correo electronico ya esta en uso')

        return redirect('appexperto:perfil', id_usuario=usuario.id)
    return render(request, 'AppExperto/perfil.html', {'usuario': usuario,
                                                      'usuario_logueado': usuario_logueado})


@login_required
def base(request):
    experto = Experto.objects.get(usuario_id=request.user.id)
    estudiantes = []
    if ExpertoFichaInformativa.objects.filter(experto_id=experto.id).exists():
        expertoFichasInformativas = ExpertoFichaInformativa.objects.filter(experto_id=experto.id)
        for expertoFichaInformativa in expertoFichasInformativas:
            estudiantes.append(Estudiante.objects.get(id=expertoFichaInformativa.estudiante.id))
    return render(request, 'AppExperto/base.html',
                  {'estudiantes': estudiantes})


@login_required
def onesignal_register(request):
    experto = Experto.objects.get(user=request.user)  # The model where you will to save the profile.
    if request.POST.get('playerId'):
        experto.onesignal_playerId = request.POST.get('playerId')
        experto.save()
        return HttpResponse('Done')
    return HttpResponse('Something went wrong')


@login_required
def verFicha(request, cedula):
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

    if request.method == 'POST':
        if bool(request.FILES.get('actividadesDocente', False)) == True:
            estudiante = Estudiante.objects.get(cedula=cedula)
            estudiante.actividadesDocente = request.FILES['actividadesDocente']
            estudiante.save()
        if bool(request.FILES.get('actividadesRepresentante', False)) == True:
            estudiante = Estudiante.objects.get(cedula=cedula)
            estudiante.actividadesRepresentante = request.FILES['actividadesRepresentante']
            estudiante.save()

    return render(request, 'AppExperto/verFichaInformativa.html',
                  {'estudiante': estudiante,
                   'fichaInformativaDocente': fichaInformativaDocente,
                   'fichaInformativaRepresentante': fichaInformativaRepresentante})


@csrf_exempt
@login_required
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
        descripcion = "Nuevo comentario de " + request.user.nombres + " para " + estudiante.nombres + " " + estudiante.apellidos
        verbRepresente = "/apprepresentante/verFichaInformativa/" + estudiante.cedula
        notify.send(request.user, recipient=docente, actor=request.user,
                    verb=verbDocente,
                    description=descripcion, target=estudiante)
        notify.send(request.user, recipient=representante, actor=request.user,
                    verb=verbRepresente,
                    description=descripcion, target=estudiante)
