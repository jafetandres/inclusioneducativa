from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from experta import KnowledgeEngine, Rule, Fact
from notifications.models import Notification
from chat.utils import create_room
from docente.forms import *
from docente.models import *
from experto.models import Comentario, ExpertoFichaInformativa
from core.forms import *


@login_required
def verFichaInformativa(request, cedula):
    if Estudiante.objects.filter(cedula=cedula).exists():
        estudiante = Estudiante.objects.get(cedula=cedula)
        if Notification.objects.filter(target_object_id=estudiante.id, recipient_id=request.user.id).exists():
            notificaciones = Notification.objects.filter(target_object_id=estudiante.id, recipient_id=request.user.id)
            for notificacion in notificaciones:
                notificacion.mark_as_read()
        fichaInformativaDocente = FichaInformativaDocente.objects.get(estudiante_id=estudiante.id)
    return render(request, 'docente/verFichaInformativa.html',
                  {'estudiante': estudiante, 'fichaInformativaDocente': fichaInformativaDocente})


@login_required
def comentarios(request):
    comentarios = Comentario.objects.filter(estudiante_id=request.GET['id']).order_by('-id')
    data1 = serializers.serialize('json', comentarios)
    return HttpResponse(data1, content_type='application/json')


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
                    docente = Docente.objects.get(usuario_id=request.user.id)
                    if FichaInformativaDocente.objects.filter(docente_id=docente.id,
                                                              estudiante_id=estudiante.id).exists() is False:
                        return redirect('appdocente:crearFichaInformativa', estudiante_cedula=estudiante.cedula)
                    elif FichaInformativaDocente.objects.filter(docente_id=docente.id,
                                                                estudiante_id=estudiante.id).exists():
                        messages.error(request, 'Usted ya ha ingresado la ficha del estudiante')
                    elif FichaInformativaDocente.objects.filter(estudiante_id=estudiante.id).exists():
                        messages.error(request, 'Otro docente ya ha ingresado la ficha del estudiante')
                else:
                    return redirect('appdocente:crearFichaInformativa', estudiante_cedula=ced)
            else:
                messages.error(request, "La cédula introducida no es válida")
    else:
        messages.error(request, "Lo sentimos no contamos con expertos por el momento")

    return render(request, 'docente/buscarEstudiante.html')


@login_required
def base(request):
    usuario_logueado = request.user
    docente = Docente.objects.get(usuario_id=usuario_logueado.id)
    fichasInformativas = FichaInformativaDocente.objects.filter(docente_id=docente.id)
    estudiantes = []
    for fichaInformativaDocente in fichasInformativas:
        if fichaInformativaDocente.docente_id == docente.id:
            estudiantes.append(Estudiante.objects.get(id=fichaInformativaDocente.estudiante_id))
    return render(request, 'docente/home.html',
                  {'estudiantes': estudiantes})


@csrf_exempt
@login_required
def perfil(request):
    usuario = Usuario.objects.get(id=request.user.id)
    docente = Docente.objects.get(usuario=usuario)
    if request.method == 'POST':
        try:
            usuario.nombres = request.POST['nombres']
            usuario.apellidos = request.POST['apellidos']
            usuario.username = request.POST['username']
            docente.tituloUniversitario = request.POST['tituloUniversitario']
            docente.experienciaProfesional = request.POST['experienciaProfesional']

            if bool(request.FILES.get('file', False)) == True:
                usuario.foto = request.FILES['file']
            usuario.email = usuario.username
            usuario.fechaNacimiento = request.POST['fechaNacimiento']
            usuario.save()
            docente.save()
        except IntegrityError as e:
            messages.error(request, 'El correo electronico ya esta en uso')

        return redirect('appdocente:perfil')
    return render(request, 'docente/perfil.html', {'docente': docente})


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
                estudiante = form_estudiante.save()
                create_room(user_list, str(estudiante.nombres + " " + estudiante.apellidos))
                return estudiante


@login_required
def crearFichaInformativa(request, estudiante_cedula):
    docente = Docente.objects.get(usuario_id=request.user.id)
    instituciones = Institucion.objects.all()
    expertos = Experto.objects.all().filter(usuario__is_active=True)
    cedula = estudiante_cedula
    estudiante = ''
    if Estudiante.objects.filter(cedula=estudiante_cedula).exists():
        estudiante = Estudiante.objects.get(cedula=estudiante_cedula)
        cedula = estudiante.cedula
    if request.method == 'POST':
        form_fichaInformativa = FichaInformativaDocenteForm(request.POST)
        form_dificultad = DificultadForm(request.POST)
        form_diagnosticoMedico = DiagnosticoMedicoForm(request.POST)
        form_diagnosticoSindromico = DiagnosticoSindromicoForm(request.POST)
        if form_fichaInformativa.is_valid() and form_dificultad.is_valid() and form_diagnosticoMedico.is_valid() and form_diagnosticoSindromico.is_valid():
            if request.POST.get('todos', False):
                user_list = Usuario.objects.filter(tipo_usuario='experto')
                form_dificultad.save()
                form_diagnosticoMedico.save()
                form_diagnosticoSindromico.save()
                fichaInformativaDocente = form_fichaInformativa.save(commit=False)
                fichaInformativaDocente.dificultad = form_dificultad.instance
                fichaInformativaDocente.diagnosticoMedico = form_diagnosticoMedico.instance
                fichaInformativaDocente.diagnosticoSindromico = form_diagnosticoSindromico.instance
                fichaInformativaDocente.docente = docente
                estudiante = crearEstudiante(request, cedula, user_list)
                fichaInformativaDocente.estudiante = estudiante
                fichaInformativaDocente.save()
                expertos = Experto.objects.all()
                for experto in expertos:
                    if ExpertoFichaInformativa.objects.filter(experto_id=experto.id,
                                                              estudiante_id=fichaInformativaDocente.estudiante.id).exists():
                        fichasInformativas = ExpertoFichaInformativa.objects.filter(experto_id=experto.id,
                                                                                    estudiante_id=fichaInformativaDocente.estudiante.id)
                        for fichaInformativa in fichasInformativas:
                            if bool(fichaInformativa.fichaInformativaDocente) == False:
                                fichaInformativa.fichaInformativaDocente = fichaInformativaDocente
                                fichaInformativa.save()
                    else:
                        expertoFichaInformativa = ExpertoFichaInformativa()
                        expertoFichaInformativa.fichaInformativaDocente = fichaInformativaDocente
                        expertoFichaInformativa.estudiante = fichaInformativaDocente.estudiante
                        expertoFichaInformativa.experto = experto
                        expertoFichaInformativa.save()
                return redirect('appdocente:base')
            elif request.POST.getlist('experto'):
                expertos = []
                user_list = []
                for id in request.POST.getlist('experto'):
                    expertos.append(Experto.objects.get(id=id))
                    user_list.append(Experto.objects.get(id=id).usuario)
                form_dificultad.save()
                form_diagnosticoMedico.save()
                form_diagnosticoSindromico.save()
                fichaInformativaDocente = form_fichaInformativa.save(commit=False)
                fichaInformativaDocente.dificultad = form_dificultad.instance
                fichaInformativaDocente.diagnosticoMedico = form_diagnosticoMedico.instance
                fichaInformativaDocente.diagnosticoSindromico = form_diagnosticoSindromico.instance
                fichaInformativaDocente.docente = docente
                estudiante = crearEstudiante(request, cedula, user_list)
                fichaInformativaDocente.estudiante = estudiante
                fichaInformativaDocente.save()
                for experto in expertos:
                    if ExpertoFichaInformativa.objects.filter(experto_id=experto.id,
                                                              estudiante_id=fichaInformativaDocente.estudiante.id).exists():
                        fichasInformativas = ExpertoFichaInformativa.objects.filter(experto_id=experto.id,
                                                                                    estudiante_id=fichaInformativaDocente.estudiante.id)
                        for fichaInformativa in fichasInformativas:
                            if bool(fichaInformativa.fichaInformativaDocente) == False:
                                fichaInformativa.fichaInformativaDocente = fichaInformativaDocente
                                fichaInformativa.save()
                    else:
                        expertoFichaInformativa = ExpertoFichaInformativa()
                        expertoFichaInformativa.fichaInformativaDocente = fichaInformativaDocente
                        expertoFichaInformativa.estudiante = fichaInformativaDocente.estudiante
                        expertoFichaInformativa.experto = experto
                        expertoFichaInformativa.save()
                create_room(user_list, str(estudiante.nombres + " " + estudiante.apellidos))
                return redirect('appdocente:base')
    return render(request, 'docente/crearFichaInformativa.html',
                  {'instituciones': instituciones, 'estudiante': estudiante, 'cedula': cedula, 'expertos': expertos})


@login_required
def editarFichaInformativa(request, estudiante_id):
    fichaInformativa = FichaInformativaDocente.objects.get(estudiante_id=estudiante_id)
    dificultad = Dificultad.objects.get(id=fichaInformativa.dificultad.id)
    diagnosticoMedico = DiagnosticoMedico.objects.get(id=fichaInformativa.diagnosticoMedico.id)
    diagnosticoSindromico = DiagnosticoSindromico.objects.get(id=fichaInformativa.diagnosticoSindromico.id)
    if request.method == 'POST':
        formfichaInformativa = FichaInformativaDocenteForm(request.POST, instance=fichaInformativa)
        formdificultad = DificultadForm(request.POST, instance=dificultad)
        formdiagnosticoMedico = DiagnosticoMedicoForm(request.POST, instance=diagnosticoMedico)
        formdiagnosticoSindromico = DiagnosticoSindromicoForm(request.POST, instance=diagnosticoSindromico)
        if formfichaInformativa.is_valid() and formdificultad.is_valid() and \
                formdiagnosticoMedico.is_valid() and formdiagnosticoSindromico.is_valid():
            fichaInformativa = formfichaInformativa.save(commit=False)
            dificultad = formdificultad.save(commit=False)
            dificultad.save()
            diagnosticoMedico = formdiagnosticoMedico.save(commit=False)
            diagnosticoMedico.save()
            diagnosticoSindromico = formdiagnosticoSindromico.save(commit=False)
            diagnosticoSindromico.save()
            fichaInformativa.dificultad = dificultad
            fichaInformativa.diagnosticoMedico = diagnosticoMedico
            fichaInformativa.diagnosticoSindromico = diagnosticoSindromico
            fichaInformativa.estudiante = Estudiante.objects.get(id=estudiante_id)
            fichaInformativa.docente = Docente.objects.get(usuario_id=request.user.id)
            fichaInformativa.save()
        messages.success(request, 'Ficha modificada exitosamente')
        return redirect('appdocente:editarFichaInformativa', estudiante_id=estudiante_id)
    else:
        fichaInformativa = FichaInformativaDocente.objects.get(estudiante_id=estudiante_id)
    return render(request, 'docente/crearFichaInformativa.html', {'fichaInformativa': fichaInformativa,
                                                                  'estudiante': fichaInformativa.estudiante
                                                                  })



# elif (request.POST['psicologo'] == 'psicologo'):
#     experto = Experto.objects.get(tituloUniversitario='psicologo')
#     expertoFichaInformativa = ExpertoFichaInformativa()
#     expertoFichaInformativa.ficha = fichaInformativaDocente
#     expertoFichaInformativa.experto = experto
#     expertoFichaInformativa.save()
# elif (request.POST['terapistaLenguaje'] == 'terapistaLenguaje'):
#     experto = Experto.objects.get(tituloUniversitario='terapistaLenguaje')
#     expertoFichaInformativa = ExpertoFichaInformativa()
#     expertoFichaInformativa.ficha = fichaInformativaDocente
#     expertoFichaInformativa.experto = experto
#     expertoFichaInformativa.save()
# elif (request.POST['terapistaFisico'] == 'terapistaFisico'):
#     experto = Experto.objects.get(tituloUniversitario='terapistaFisico')
#     expertoFichaInformativa = ExpertoFichaInformativa()
#     expertoFichaInformativa.ficha = fichaInformativaDocente
#     expertoFichaInformativa.experto = experto
#     expertoFichaInformativa.save()
# elif (request.POST['educador'] == 'educador'):
#     experto = Experto.objects.get(tituloUniversitario='educador')
#     expertoFichaInformativa = ExpertoFichaInformativa()
#     expertoFichaInformativa.ficha = fichaInformativaDocente
#     expertoFichaInformativa.experto = experto
#     expertoFichaInformativa.save()
# elif (request.POST['estimuladorTemprano'] == 'estimuladorTemprano'):
#     experto = Experto.objects.get(tituloUniversitario='estimuladorTemprano')
#     expertoFichaInformativa = ExpertoFichaInformativa()
#     expertoFichaInformativa.ficha = fichaInformativaDocente
#     expertoFichaInformativa.experto = experto
#     expertoFichaInformativa.save()
# chatusuarios.append(Usuario.objects.get(id=expertoFichaInformativa.experto.usuario.id))

# notificaion = Notificacion()
# notificaion.receptor = usuario
# notificaion.emisor = request.user
#
# notificaion.visto = False
# notificaion.target = estudiante.id
# notificaion.descripcion = 'NUEVO CASO'
#
# notificaion.save()
#
#

# create_room(chatusuarios)

#
# elif (request.POST['psicologo'] == 'psicologo'):
#
# # experto = Experto.objects.filter(tituloUniversitario='PSICOLOGO')
# # notificaion.receptor = experto
#
# elif (request.POST['terapistaLenguaje'] == 'terapistaLenguaje'):
#
# # experto = Experto.objects.filter(tituloUniversitario='TERAPISTA DE LENGUAJE')
# # notificaion.receptor = experto
#
# elif (request.POST['docente'] == 'docente'):
#
# # experto = Experto.objects.filter(tituloUniversitario='DOCENTE')
# # notificaion.receptor = experto
#
# elif (request.POST['fonoaudiologo'] == 'fonoaudiologo'):

# experto = Experto.objects.filter(tituloUniversitario='FONOAUDIOLOGO')
# notificaion.receptor = experto

# notify.send(request.user, recipient_list=expertos.usuario, verb='Un nuevo caso llego.', target=estudiante)

# def EstudianteTest(request):
#     if request.method == 'POST':
#         p1 = request.POST.get('p1r1')
#         p2 = request.POST.get('p1r2')
#         p3 = request.POST.get('p1r3')
#         p4 = request.POST.get('p1r4')
#         p5 = request.POST.get('p1r5')
#
#         p6 = request.POST.get('p2r1')
#         p7 = request.POST.get('p2r2')
#         p8 = request.POST.get('p2r3')
#
#         p9 = request.POST.get('p3r1')
#         p10 = request.POST.get('p3r2')
#
#         p11 = request.POST.get('p4r1')
#         p12 = request.POST.get('p4r2')
#         p13 = request.POST.get('p4r3')
#
#         p14 = request.POST.get('p5r1')
#         p15 = request.POST.get('p5r2')
#         p16 = request.POST.get('p5r3')
#         p17 = request.POST.get('p5r4')
#         p18 = request.POST.get('p5r5')
#
#         p19 = request.POST.get('p6r1')
#         p20 = request.POST.get('p6r2')
#         p21 = request.POST.get('p6r3')
#         p22 = request.POST.get('p6r4')
#         p23 = request.POST.get('p6r5')
#         p24 = request.POST.get('p6r6')
#         p25 = request.POST.get('p6r7')
#         p26 = request.POST.get('p6r8')
#         p27 = request.POST.get('p6r9')
#         p28 = request.POST.get('p6r10')
#
#         p29 = request.POST.get('p7r1')
#         p30 = request.POST.get('p7r2')
#         p31 = request.POST.get('p7r3')
#         p32 = request.POST.get('p7r4')
#         p33 = request.POST.get('p7r5')
#         p34 = request.POST.get('p7r6')
#         p35 = request.POST.get('p7r7')
#         p36 = request.POST.get('p7r8')
#         p37 = request.POST.get('p7r9')
#         p38 = request.POST.get('p7r10')
#         p39 = request.POST.get('p7r11')
#         p40 = request.POST.get('p7r12')
#         p41 = request.POST.get('p7r13')
#         p42 = request.POST.get('p7r14')
#         p43 = request.POST.get('p7r15')
#
#         p44 = request.POST.get('p8r1')
#         p45 = request.POST.get('p8r2')
#         p46 = request.POST.get('p8r3')
#         p47 = request.POST.get('p8r4')
#         p48 = request.POST.get('p8r5')
#         p49 = request.POST.get('p8r6')
#         p50 = request.POST.get('p8r7')
#
#         engenie = RobotCrossStreet()
#         engenie.reset()
#         engenie.declare(P1(respuesta=p1))
#
#         engenie.declare(P2(respuesta=[p2, p3, p5, p10, p15, p16, p17, p18, p30, p37, p41,
#                                              p42]))
#
#         engenie.run()
#         engenie.reset()
#
#         return redirect('appdocente:resultado_test')
#
#     return render(request, 'docente/estudiante_test.html')
