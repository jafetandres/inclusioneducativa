from random import choice
from urllib import request
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from experta import *
from notifications.models import Notification

from InclusionEducativa.Apps.AppDocente.forms import *
from InclusionEducativa.Apps.AppDocente.models import *
from InclusionEducativa.Apps.AppExperto.models import Comentario
from InclusionEducativa.Apps.GestionSistema.models import *
from InclusionEducativa.Apps.GestionSistema.forms import *
from django_chatter.utils import create_room

contador = 0


def verFichaInformativa(request, cedula):
    usuario_logueado = request.user
    if Estudiante.objects.filter(cedula=cedula).exists():
        estudiante = Estudiante.objects.get(cedula=cedula)
        if Notification.objects.filter(target_object_id=estudiante.id, recipient_id=request.user.id).exists():
            notificaciones = Notification.objects.filter(target_object_id=estudiante.id, recipient_id=request.user.id)
            for notificacion in notificaciones:
                notificacion.mark_as_read()
        fichaInformativaDocente = FichaInformativaDocente.objects.get(estudiante_id=estudiante.id)
    # comentarios = Comentario.objects.filter(estudiante_id=estudiante.id).order_by('-id')
    return render(request, 'AppDocente/verFichaInformativa.html',
                  {'estudiante': estudiante, 'fichaInformativaDocente': fichaInformativaDocente,
                   'usuario_logueado': usuario_logueado})


def comentarios(request):
    print(request.GET['id'])
    comentarios = Comentario.objects.filter(estudiante_id=request.GET['id']).order_by('-id')
    data1 = serializers.serialize('json', comentarios)
    return HttpResponse(data1, content_type='application/json')


def buscarEstudiante(request):
    docente = Docente.objects.get(usuario_id=request.user.id)
    usuario_logueado = request.user
    if request.method == 'POST':
        ced = request.POST['cedula']
        valores = [int(ced[x]) * (2 - x % 2) for x in range(9)]
        suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
        if int(ced[9]) == 10 - int(str(suma)[-1:]):
            if Estudiante.objects.filter(cedula=request.POST['cedula']).exists():
                estudiante = Estudiante.objects.get(cedula=request.POST['cedula'])
                return render(request, 'AppDocente/crearFichaInformativa.html',
                              {'usuario_logueado': usuario_logueado, 'estudiante': estudiante})
                if FichaInformativa.objects.filter(docente_id=docente.id, estudiante_id=estudiante.id).exists():
                    messages.error(request, 'Ya ha ingresado la ficha del estudiante')
            else:
                instituciones = Institucion.objects.all()
                return redirect('appdocente:crearFichaInformativa')
                # return render(request, 'AppDocente/crearFichaInformativa.html',
                #               {'usuario_logueado': usuario_logueado, 'instituciones': instituciones})
        else:
            messages.error(request, "La cédula introducida no es válida")
    return render(request, 'AppDocente/buscarEstudiante.html', {'usuario_logueado': usuario_logueado})


class Pregunta1(Fact):
    """informacion hacerca de la primera posibilidad"""
    pass


class Pregunta2(Fact):
    """informacion hacerca de la segunda posibilidad"""
    pass


class RobotCrossStreet(KnowledgeEngine):

    @Rule((Pregunta1(respuesta=['p1', 'p4', 'p6', 'p7', 'p8', 'p9', 'p11', 'p12', 'p13', 'p14', 'p19',
                                'p20', 'p21', 'p22', 'p23', 'p24', 'p25', 'p26', 'p27', 'p28', 'p29', 'p31',
                                'p32', 'p33', 'p34', 'p35', 'p36', 'p38', 'p39', 'p40', 'p43', 'p44', 'p45', 'p46',
                                'p47', 'p48', 'p49', 'p50'])))
    def a(self):
        global contador
        contador = 1

    @Rule((Pregunta2(respuesta=['p2', 'p3', 'p5', 'p10', 'p15', 'p16', 'p17', 'p18', 'p30', 'p37', 'p41',
                                'p42'])))
    def b(self):
        global contador
        contador = 2


def base(request):
    usuario_logueado = request.user
    docente = Docente.objects.get(usuario_id=usuario_logueado.id)
    fichasInformativas = FichaInformativaDocente.objects.filter(docente_id=docente.id)
    estudiantes = []
    for fichaInformativaDocente in fichasInformativas:
        if fichaInformativaDocente.docente_id == docente.id:
            estudiantes.append(Estudiante.objects.get(id=fichaInformativaDocente.estudiante_id))
    return render(request, 'AppDocente/base.html',
                  {'usuario_logueado': usuario_logueado, 'estudiantes': estudiantes})


def EstudianteTest(request):
    print('entro')
    if request.method == 'POST':
        p1 = request.POST.get('p1r1')
        p2 = request.POST.get('p1r2')
        p3 = request.POST.get('p1r3')
        p4 = request.POST.get('p1r4')
        p5 = request.POST.get('p1r5')

        p6 = request.POST.get('p2r1')
        p7 = request.POST.get('p2r2')
        p8 = request.POST.get('p2r3')

        p9 = request.POST.get('p3r1')
        p10 = request.POST.get('p3r2')

        p11 = request.POST.get('p4r1')
        p12 = request.POST.get('p4r2')
        p13 = request.POST.get('p4r3')

        p14 = request.POST.get('p5r1')
        p15 = request.POST.get('p5r2')
        p16 = request.POST.get('p5r3')
        p17 = request.POST.get('p5r4')
        p18 = request.POST.get('p5r5')

        p19 = request.POST.get('p6r1')
        p20 = request.POST.get('p6r2')
        p21 = request.POST.get('p6r3')
        p22 = request.POST.get('p6r4')
        p23 = request.POST.get('p6r5')
        p24 = request.POST.get('p6r6')
        p25 = request.POST.get('p6r7')
        p26 = request.POST.get('p6r8')
        p27 = request.POST.get('p6r9')
        p28 = request.POST.get('p6r10')

        p29 = request.POST.get('p7r1')
        p30 = request.POST.get('p7r2')
        p31 = request.POST.get('p7r3')
        p32 = request.POST.get('p7r4')
        p33 = request.POST.get('p7r5')
        p34 = request.POST.get('p7r6')
        p35 = request.POST.get('p7r7')
        p36 = request.POST.get('p7r8')
        p37 = request.POST.get('p7r9')
        p38 = request.POST.get('p7r10')
        p39 = request.POST.get('p7r11')
        p40 = request.POST.get('p7r12')
        p41 = request.POST.get('p7r13')
        p42 = request.POST.get('p7r14')
        p43 = request.POST.get('p7r15')

        p44 = request.POST.get('p8r1')
        p45 = request.POST.get('p8r2')
        p46 = request.POST.get('p8r3')
        p47 = request.POST.get('p8r4')
        p48 = request.POST.get('p8r5')
        p49 = request.POST.get('p8r6')
        p50 = request.POST.get('p8r7')

        engenie = RobotCrossStreet()
        engenie.reset()
        engenie.declare(Pregunta1(respuesta=[p1, p4, p6, p7, p8, p9, p11, p12, p13, p14, p19,
                                             p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p31,
                                             p32, p33, p34, p35, p36, p38, p39, p40, p43, p44, p45, p46,
                                             p47, p48, p49, p50]))

        engenie.declare(Pregunta2(respuesta=[p2, p3, p5, p10, p15, p16, p17, p18, p30, p37, p41,
                                             p42]))

        engenie.run()
        engenie.reset()

        return redirect('appdocente:resultado_test')

    return render(request, 'AppDocente/estudiante_test.html')


def ResultadoTest(request):
    global contador
    resultado = ''
    if contador == 1:
        resultado = 'EL RESULTADO INTERFIERE NEGATIVAMENTE EN LA INCLUSIÓN'

    elif contador == 2:
        resultado = 'EL RESULTADO NO INTERFIERE NEGATIVAMENTE EN LA INCLUSIÓN'

    else:
        resultado = 'El niño necesita un diagnóstico personalizado.'

    contador = 0

    return render(request, 'AppDocente/resultado_test.html', {'resultado': resultado})


def perfil(request, id_usuario):
    usuario_logueado = request.user
    usuario = Usuario.objects.get(id=request.user.id)
    form_usuario = UsuarioForm(request.POST, instance=usuario)
    if request.method == 'POST':
        if form_usuario.is_valid():
            form_usuario.save()
        return redirect('appdocente:base')
    return render(request, 'AppDocente/perfil.html', {'usuario': usuario,
                                                      'usuario_logueado': usuario_logueado})


def crearEstudiante(request, cedula):
    if request.method == 'POST':
        if Estudiante.objects.filter(cedula=cedula).exists():
            estudiante = Estudiante.objects.get(cedula=cedula)
            return estudiante
        else:
            form_estudiante = EstudianteForm(request.POST)
            if form_estudiante.is_valid():
                estudiante = form_estudiante.save()
                return estudiante


def crearFichaInformativa(request):
    usuario_logueado = request.user
    docente = Docente.objects.get(usuario_id=request.user.id)
    if request.method == 'POST':
        cedula = request.POST['cedula']
        form_fichaInformativa = FichaInformativaForm(request.POST)
        form_dificultad = DificultadForm(request.POST)
        form_diagnosticoMedico = DiagnosticoMedicoForm(request.POST)
        form_diagnosticoSindromico = DiagnosticoSindromicoForm(request.POST)
        if form_fichaInformativa.is_valid() and form_dificultad.is_valid() and form_diagnosticoMedico.is_valid() and form_diagnosticoSindromico.is_valid():
            form_dificultad.save()
            form_diagnosticoMedico.save()
            form_diagnosticoSindromico.save()
            fichaInformativaDocente = form_fichaInformativa.save(commit=False)
            fichaInformativaDocente.dificultad = form_dificultad.instance
            fichaInformativaDocente.diagnosticoMedico = form_diagnosticoMedico.instance
            fichaInformativaDocente.diagnosticoSindromico = form_diagnosticoSindromico.instance
            fichaInformativaDocente.docente = docente
            fichaInformativaDocente.estudiante = crearEstudiante(request, cedula)
            fichaInformativaDocente.save()
            if (request.POST['todos'] == 'todos'):
                expertos = Experto.objects.all()
                for experto in expertos:
                    expertoFicha = ExpertoFichaInformativa()
                    expertoFicha.ficha = fichaInformativaDocente
                    expertoFicha.experto = experto
                    expertoFicha.save()
            elif (request.POST['psicologo'] == 'psicologo'):
                experto = Experto.objects.get(tituloUniversitario='PSICOLOGO')
                expertoFicha = ExpertoFichaInformativa()
                expertoFicha.ficha = fichaInformativaDocente
                expertoFicha.experto = experto
                expertoFicha.save()

            elif (request.POST['terapistaLenguaje'] == 'terapistaLenguaje'):
                experto = Experto.objects.get(tituloUniversitario='TERAPISTA DE LENGUAJE')
                expertoFicha = ExpertoFichaInformativa()
                expertoFicha.ficha = fichaInformativaDocente
                expertoFicha.experto = experto
                expertoFicha.save()
            elif (request.POST['terapistaFisico'] == 'terapistaFisico'):
                experto = Experto.objects.get(tituloUniversitario='TERAPISTA FISICO')
                expertoFicha = ExpertoFichaInformativa()
                expertoFicha.ficha = fichaInformativaDocente
                expertoFicha.experto = experto
                expertoFicha.save()
            elif (request.POST['educador'] == 'educador'):
                experto = Experto.objects.get(tituloUniversitario='EDUCADOR')
                expertoFicha = ExpertoFichaInformativa()
                expertoFicha.ficha = fichaInformativaDocente
                expertoFicha.experto = experto
                expertoFicha.save()
            elif (request.POST['estimulador'] == 'estimulador'):
                experto = Experto.objects.get(tituloUniversitario='ESTIMULADOR TEMPRANO')
                expertoFicha = ExpertoFichaInformativa()
                expertoFicha.ficha = fichaInformativaDocente
                expertoFicha.experto = experto
                expertoFicha.save()
                # chatusuarios.append(Usuario.objects.get(id=expertoFicha.experto.usuario.id))

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

        return redirect('appdocente:base')
    else:
        instituciones = Institucion.objects.all()
    return render(request, 'AppDocente/crearFichaInformativa.html',
                  {'usuario_logueado': usuario_logueado,
                   'instituciones': instituciones
                   })


def EstudianteEditar(request, id_estudiante):
    estudiante = EstudianteDocente.objects.get(id=id_estudiante)
    if request.method == 'POST':
        form = fichaEstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
        return redirect('appdocente:base')
    return render(request, 'AppDocente/estudiante_crear.htm', {'form_estudiante': estudiante})


def fichaEstudianteListar(request):
    fichasEstudiantes = EstudianteDocente.objects.all()
    return render(request, 'AppDocente/fichaEstudianteListar.html', {'fichasEstudiantes': fichasEstudiantes})


def EstudianteEliminar(request, id_estudiante):
    estudiante = EstudianteDocente.objects.get(id=id_estudiante)
    if request.method == 'POST':
        estudiante.delete()
        return redirect('appdocente:estudiante_listar')
    return render(request, 'AppDocente/estudiante_eliminar.html', {'estudiante': estudiante})
