from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from notifications.models import Notification
from chat.utils import create_room
from experto.models import ExpertoFichaInformativa
from representante.forms import *
from representante.models import *
from core.forms import EstudianteForm
from core.models import *


@csrf_exempt
@login_required
def perfil(request):
    usuario = Usuario.objects.get(id=request.user.id)
    representante=Representante.objects.get(usuario=usuario)
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
    return render(request, 'representante/perfil.html', {'representante':representante})


@login_required
def buscarEstudiante(request):
    if Experto.objects.all().exists():
        if request.method == 'POST':
            ced = request.POST['cedula']
            valores = [int(ced[x]) * (2 - x % 2) for x in range(9)]
            suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
            if int(ced[9]) == 10 - int(str(suma)[-1:]):
                if Estudiante.objects.filter(cedula=request.POST['cedula']).exists():
                    estudiante = Estudiante.objects.get(cedula=request.POST['cedula'])
                    representante = Representante.objects.get(usuario_id=request.user.id)
                    if FichaInformativaRepresentante.objects.filter(representante_id=representante.id,
                                                                    estudiante_id=estudiante.id).exists() is False:
                        return redirect('apprepresentante:crearFichaInformativa',
                                        estudiante_cedula=estudiante.cedula)
                    elif FichaInformativaRepresentante.objects.filter(representante_id=representante.id,
                                                                      estudiante_id=estudiante.id).exists():
                        messages.error(request, 'Usted ya ha ingresado la ficha de su hijo(a)')
                    elif FichaInformativaRepresentante.objects.filter(estudiante_id=estudiante.id).exists():
                        messages.error(request, 'Otro representante ya ha ingresado la ficha del niño(a)')
                else:
                    return redirect('apprepresentante:crearFichaInformativa', estudiante_cedula=ced)
            else:
                messages.error(request, "La cédula introducida no es válida")
    else:
        messages.error(request, "Lo sentimos no contamos con expertos disponibles por el momento")
    return render(request, 'representante/buscarEstudiante.html')


@login_required
def base(request):
    representante = Representante.objects.get(usuario_id=request.user.id)
    fichasInformativas = FichaInformativaRepresentante.objects.filter(representante_id=representante.id)
    estudiantes = []
    for fichaInformativaRepresentante in fichasInformativas:
        if fichaInformativaRepresentante.representante_id == representante.id:
            estudiantes.append(Estudiante.objects.get(id=fichaInformativaRepresentante.estudiante_id))
    return render(request, 'representante/home.html',
                  {'estudiantes': estudiantes})


@login_required
def crearEstudiante(request, cedula, user_list):
    if request.method == 'POST':
        if Estudiante.objects.filter(cedula=cedula).exists():
            estudiante = Estudiante.objects.get(cedula=cedula)
            return estudiante
        else:
            form_estudiante = EstudianteForm(request.POST)
            if form_estudiante.is_valid():
                estudiante = form_estudiante.save(commit=False)
                estudiante.cedula = cedula
                estudiante.estado = 'nuevo'
                estudiante = form_estudiante.save()
                create_room(user_list, str(estudiante.nombres + " " + estudiante.apellidos))
                return estudiante


@login_required
def crearFichaInformativa(request, estudiante_cedula):
    representante = Representante.objects.get(usuario_id=request.user.id)
    cedula = estudiante_cedula
    expertos = Experto.objects.all()
    estudiante = ''
    if Estudiante.objects.filter(cedula=estudiante_cedula).exists():
        estudiante = Estudiante.objects.get(cedula=estudiante_cedula)
        cedula = estudiante.cedula
    if request.method == 'POST':
        form_fichaInformativaRepresentante = FichaInformativaRepresentanteForm(request.POST)
        form_dificultad = DificultadForm(request.POST)
        form_diagnosticoMedico = DiagnosticoMedicoForm(request.POST)
        if form_fichaInformativaRepresentante.is_valid() and form_dificultad.is_valid() and form_diagnosticoMedico.is_valid():
            if request.POST.get('todos', False):
                user_list = Usuario.objects.filter(tipo_usuario='experto')
                form_dificultad.save()
                form_diagnosticoMedico.save()
                fichaInformativaRepresentante = form_fichaInformativaRepresentante.save(commit=False)
                fichaInformativaRepresentante.dificultad = form_dificultad.instance
                fichaInformativaRepresentante.diagnosticoMedico = form_diagnosticoMedico.instance
                fichaInformativaRepresentante.representante = representante
                fichaInformativaRepresentante.estudiante = crearEstudiante(request, cedula, user_list)
                fichaInformativaRepresentante.save()
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
            elif request.POST.getlist('experto'):
                user_list = []
                expertos = []
                for id in request.POST.getlist('experto'):
                    expertos.append(Experto.objects.get(id=id))
                    user_list.append(Experto.objects.get(id=id).usuario)
                form_dificultad.save()
                form_diagnosticoMedico.save()
                fichaInformativaRepresentante = form_fichaInformativaRepresentante.save(commit=False)
                fichaInformativaRepresentante.dificultad = form_dificultad.instance
                fichaInformativaRepresentante.diagnosticoMedico = form_diagnosticoMedico.instance
                fichaInformativaRepresentante.representante = representante
                fichaInformativaRepresentante.estudiante = crearEstudiante(request, cedula, user_list)
                fichaInformativaRepresentante.save()

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
    return render(request, 'representante/crearFichaInformativa.html',
                  {'instituciones': instituciones, 'estudiante': estudiante, 'cedula': cedula, 'expertos': expertos})


@login_required
def verFichaInformativa(request, cedula):
    if Estudiante.objects.filter(cedula=cedula).exists():
        estudiante = Estudiante.objects.get(cedula=cedula)
        if Notification.objects.filter(target_object_id=estudiante.id, recipient_id=request.user.id).exists():
            notificaciones = Notification.objects.filter(target_object_id=estudiante.id, recipient_id=request.user.id)
            for notificacion in notificaciones:
                notificacion.mark_as_read()
        fichaInformativaRepresentante = FichaInformativaRepresentante.objects.get(estudiante_id=estudiante.id)
    return render(request, 'representante/verFichaInformativa.html',
                  {'estudiante': estudiante, 'fichaInformativaRepresentante': fichaInformativaRepresentante})


@login_required
def editarFichaInformativa(request, estudiante_id):
    fichaInformativa = FichaInformativaRepresentante.objects.get(estudiante_id=estudiante_id)
    dificultad = Dificultad.objects.get(id=fichaInformativa.dificultad.id)
    diagnosticoMedico = DiagnosticoMedico.objects.get(id=fichaInformativa.diagnosticoMedico.id)
    if request.method == 'POST':
        formfichaInformativa = FichaInformativaRepresentanteForm(request.POST, instance=fichaInformativa)
        formdificultad = DificultadForm(request.POST, instance=dificultad)
        formdiagnosticoMedico = DiagnosticoMedicoForm(request.POST, instance=diagnosticoMedico)
        if formfichaInformativa.is_valid() and formdificultad.is_valid() and \
                formdiagnosticoMedico.is_valid():
            fichaInformativa = formfichaInformativa.save(commit=False)
            dificultad = formdificultad.save(commit=False)
            dificultad.save()
            diagnosticoMedico = formdiagnosticoMedico.save(commit=False)
            diagnosticoMedico.save()
            fichaInformativa.dificultad = dificultad
            fichaInformativa.diagnosticoMedico = diagnosticoMedico
            fichaInformativa.estudiante = Estudiante.objects.get(id=estudiante_id)
            fichaInformativa.representante = Representante.objects.get(usuario_id=request.user.id)
            fichaInformativa.save()
        messages.success(request, 'Ficha modificada exitosamente')
        return redirect('apprepresentante:editarFichaInformativa', estudiante_id=estudiante_id)
    else:
        fichaInformativa = FichaInformativaRepresentante.objects.get(estudiante_id=estudiante_id)
    return render(request, 'representante/crearFichaInformativa.html', {'fichaInformativa': fichaInformativa,
                                                                           'estudiante': fichaInformativa.estudiante
                                                                           })
