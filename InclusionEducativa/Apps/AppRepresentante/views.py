from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django_chatter.models import Room
from django_chatter.utils import create_room
from notifications.models import Notification
from InclusionEducativa.Apps.AppExperto.models import ExpertoFichaInformativa
from InclusionEducativa.Apps.AppRepresentante.forms import *
from InclusionEducativa.Apps.AppRepresentante.models import *
from InclusionEducativa.Apps.GestionSistema.forms import EstudianteForm
from InclusionEducativa.Apps.GestionSistema.models import *


@csrf_exempt
@login_required
def perfil(request):
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
        return redirect('apprepresentante:perfil')
    return render(request, 'AppRepresentante/perfil.html')


@login_required
def buscarEstudiante(request):
    if request.method == 'POST':
        if Experto.objects.all().exists():
            ced = request.POST['cedula']
            valores = [int(ced[x]) * (2 - x % 2) for x in range(9)]
            suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
            if int(ced[9]) == 10 - int(str(suma)[-1:]):
                if Estudiante.objects.filter(cedula=request.POST['cedula']).exists():
                    estudiante = Estudiante.objects.get(cedula=request.POST['cedula'])
                    representante = Representante.objects.get(usuario_id=request.user.id)
                    if FichaInformativaRepresentante.objects.filter(representante_id=representante.id,
                                                                    estudiante_id=estudiante.id).exists() is False:
                        return redirect('apprepresentante:crearFichaInformativa', estudiante_cedula=estudiante.cedula)
                    else:
                        if FichaInformativaRepresentante.objects.filter(estudiante_id=estudiante.id).exists():
                            messages.error(request, 'Ya ha ingresado la ficha del estudiante otro representante')
                        else:
                            messages.error(request, 'Usted ya ha ingresado la ficha del estudiante')
                else:
                    return redirect('apprepresentante:crearFichaInformativa', estudiante_cedula=ced)
            else:
                messages.error(request, "La cédula introducida no es válida")
        else:
            messages.error(request, "Lo sentimos no contamos con expertos disponibles por el momento")
    return render(request, 'AppRepresentante/buscarEstudiante.html')


@login_required
def base(request):
    representante = Representante.objects.get(usuario_id=request.user.id)
    fichasInformativas = FichaInformativaRepresentante.objects.filter(representante_id=representante.id)
    estudiantes = []
    for fichaInformativaRepresentante in fichasInformativas:
        if fichaInformativaRepresentante.representante_id == representante.id:
            estudiantes.append(Estudiante.objects.get(id=fichaInformativaRepresentante.estudiante_id))
    return render(request, 'AppRepresentante/base.html',
                  {'estudiantes': estudiantes})


@login_required
def crearEstudiante(request, cedula):
    if request.method == 'POST':
        if Estudiante.objects.filter(cedula=cedula).exists():
            estudiante = Estudiante.objects.get(cedula=cedula)
            return estudiante
        else:
            form_estudiante = EstudianteForm(request.POST)
            if form_estudiante.is_valid():
                estudiante = form_estudiante.save(commit=False)
                estudiante.cedula = cedula
                estudiante = form_estudiante.save()
                # crear_room(estudiante, 'nuevo')
                return estudiante


# @login_required
# def crear_room(estudiante, estado):
#     usuarios = Usuario.objects.filter(tipo_usuario='experto')
#     room_id = create_room(usuarios, estado)
#     room = Room.objects.get(id=room_id)
#     room.name = 'Caso ' + estudiante.nombres + ' ' + estudiante.apellidos
#     room.save()

@login_required
def crearFichaInformativa(request, estudiante_cedula):
    representante = Representante.objects.get(usuario_id=request.user.id)
    cedula = estudiante_cedula
    estudiante = None
    if Estudiante.objects.filter(cedula=estudiante_cedula).exists():
        estudiante = Estudiante.objects.get(cedula=estudiante_cedula)
        cedula = estudiante.cedula
    if request.method == 'POST':
        form_fichaInformativaRepresentante = FichaInformativaRepresentanteForm(request.POST)
        form_dificultad = DificultadForm(request.POST)
        form_diagnosticoMedico = DiagnosticoMedicoForm(request.POST)
        if form_fichaInformativaRepresentante.is_valid() and form_dificultad.is_valid() and form_diagnosticoMedico.is_valid():
            form_dificultad.save()
            form_diagnosticoMedico.save()
            fichaInformativaRepresentante = form_fichaInformativaRepresentante.save(commit=False)
            fichaInformativaRepresentante.dificultad = form_dificultad.instance
            fichaInformativaRepresentante.diagnosticoMedico = form_diagnosticoMedico.instance
            fichaInformativaRepresentante.representante = representante
            fichaInformativaRepresentante.estudiante = crearEstudiante(request, cedula)
            fichaInformativaRepresentante.save()
            # if (request.POST['todos'] == 'todos'):
            expertos = Experto.objects.all()
            for experto in expertos:
                if ExpertoFichaInformativa.objects.filter(experto_id=experto.id,
                                                          estudiante_id=fichaInformativaRepresentante.estudiante.id).exists():
                    fichasInformativas = ExpertoFichaInformativa.objects.filter(experto_id=experto.id,
                                                                                estudiante_id=fichaInformativaRepresentante.estudiante.id)

                    for fichaInformativa in fichasInformativas:
                        if bool(fichaInformativa.fichaInformativaRepresentante) == False:
                            fichaInformativa.fichaInformativaRepresentante = fichaInformativaRepresentante
                            fichaInformativa.save()
                else:
                    expertoFichaInformativa = ExpertoFichaInformativa()
                    expertoFichaInformativa.fichaInformativaRepresentante = fichaInformativaRepresentante
                    expertoFichaInformativa.estudiante = fichaInformativaRepresentante.estudiante
                    expertoFichaInformativa.experto = experto
                    expertoFichaInformativa.save()
            return redirect('apprepresentante:base')
    else:
        instituciones = Institucion.objects.all()
    return render(request, 'AppRepresentante/crearFichaInformativa.html',
                  {'instituciones': instituciones, 'estudiante': estudiante, 'cedula': cedula})


@login_required
def verFichaInformativa(request, cedula):
    if Estudiante.objects.filter(cedula=cedula).exists():
        estudiante = Estudiante.objects.get(cedula=cedula)
        if Notification.objects.filter(target_object_id=estudiante.id, recipient_id=request.user.id).exists():
            notificaciones = Notification.objects.filter(target_object_id=estudiante.id, recipient_id=request.user.id)
            for notificacion in notificaciones:
                notificacion.mark_as_read()
        fichaInformativaRepresentante = FichaInformativaRepresentante.objects.get(estudiante_id=estudiante.id)
    return render(request, 'AppRepresentante/verFichaInformativa.html',
                  {'estudiante': estudiante, 'fichaInformativaRepresentante': fichaInformativaRepresentante})
