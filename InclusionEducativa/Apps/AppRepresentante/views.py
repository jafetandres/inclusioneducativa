from django.shortcuts import render, redirect
from InclusionEducativa.Apps.AppRepresentante.forms import *
from InclusionEducativa.Apps.GestionSistema.models import *


def base(request):
    usuario_logueado = request.user
    representante = Representante.objects.get(usuario_id=usuario_logueado.id)

    fichas_estudianteshas_estudiantes = EstudianteRepresentante.objects.filter(representante_id=representante.id)
    return render(request, 'AppRepresentante/base.html',
                  {'usuario_logueado': usuario_logueado, 'fichas_estudiantes': fichas_estudiantes})


def fichaEstudianteCrear(request):
    usuario_logueado = request.user

    representante = Representante.objects.get(usuario_id=request.user.id)

    if request.method == 'POST':
        form_estudiante = FichaEstudianteForm(request.POST)
        form_dificultad = DificultadForm(request.POST)
        form_diagnosticoMedico = DiagnosticoMedicoForm(request.POST)

        if request.POST['antecedentesFPatologicos'] == 'Si':
            request.POST._mutable = True
            form_estudiante.antecedentesFPatologicos = 'Si:  ' + request.POST['descripcionAntecedentesFPatologicos']
            request.POST._mutable = False

        if form_estudiante.is_valid() and form_dificultad.is_valid() and form_diagnosticoMedico.is_valid():
            form_dificultad.save()
            form_diagnosticoMedico.save()

            estudiante = form_estudiante.save(commit=False)
            estudiante.dificultad = form_dificultad.instance
            estudiante.diagnosticoMedico = form_diagnosticoMedico.instance
            estudiante.representante = representante
            estudiante.institucion = representante.institucion

            form_estudiante.save()

            if (request.POST['todos'] == 'todos'):
                expertos = Experto.objects.all()
                # chatusuarios=[]
                for experto in expertos:
                    expertoFicha = Representante_ExpertoFicha()
                    expertoFicha.ficha = estudiante
                    expertoFicha.experto = experto
                    expertoFicha.save()

            elif (request.POST['psicologo'] == 'psicologo'):
                experto = Experto.objects.get(tituloUniversitario='PSICOLOGO')

                expertoFicha = Representante_ExpertoFicha()
                expertoFicha.ficha = estudiante
                expertoFicha.experto = experto
                expertoFicha.save()

            elif (request.POST['terapistaLenguaje'] == 'terapistaLenguaje'):
                experto = Experto.objects.get(tituloUniversitario='TERAPISTA DE LENGUAJE')

                expertoFicha = Representante_ExpertoFicha()
                expertoFicha.ficha = estudiante
                expertoFicha.experto = experto
                expertoFicha.save()

            elif (request.POST['terapistaFisico'] == 'terapistaFisico'):
                experto = Experto.objects.get(tituloUniversitario='TERAPISTA FISICO')

                expertoFicha = Representante_ExpertoFicha()
                expertoFicha.ficha = estudiante
                expertoFicha.experto = experto
                expertoFicha.save()

            elif (request.POST['educador'] == 'educador'):
                experto = Experto.objects.get(tituloUniversitario='EDUCADOR')

                expertoFicha = Representante_ExpertoFicha()
                expertoFicha.ficha = estudiante
                expertoFicha.experto = experto
                expertoFicha.save()

            elif (request.POST['estimulador'] == 'estimulador'):
                experto = Experto.objects.get(tituloUniversitario='ESTIMULADOR TEMPRANO')

                expertoFicha = Representante_ExpertoFicha()
                expertoFicha.ficha = estudiante
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

        return redirect('apprepresentante:base')
    else:
        form_estudiante = FichaEstudianteForm()
        form_dificultad = DificultadForm()
        form_diagnosticoMedico = DiagnosticoMedicoForm()

    return render(request, 'AppRepresentante/fichaEstudianteCrear.html',
                  {'form_estudiante': form_estudiante, 'form_dificultad': form_dificultad,
                   'form_diagnosticoMedico': form_diagnosticoMedico,
                   'usuario_logueado': usuario_logueado
                   })
