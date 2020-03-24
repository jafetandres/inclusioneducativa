from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, redirect
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from InclusionEducativa.Apps.AppExperto.models import Comentario
from InclusionEducativa.Apps.AppRepresentante.models import *
from InclusionEducativa.Apps.AppDocente.models import EstudianteDocente, ExpertoFicha
from InclusionEducativa.Apps.GestionSistema.models import *

notificaciones = None


def perfil(request):
    usuario_logueado = request.user
    experto = Experto.objects.get(usuario_id=request.user.id)
    # form_usuario = UsuarioForm(request.POST, instance=experto)
    # if request.method == 'POST':
    #     if form_usuario.is_valid():
    #         form_usuario.save()
    #
    #     return redirect('gestionsistema:base')
    return render(request, 'AppExperto/perfil.html', {'experto': experto,
                                                          'usuario_logueado': usuario_logueado})



def base(request):
    global notificaciones
    usuario_logueado = request.user
    # fichas_estudiantes=None

    experto = Experto.objects.get(usuario_id=request.user
                                  .id)

    fichas_estudiantes = ExpertoFicha.objects.filter(experto_id=experto.id)
    # esttudianteDocente = EstudianteDocente()
    # fichas_estudiantes=expertoFichas.ficha
    #

    # for expertoFicha in expertoFichas:
    #     esttudianteDocente=EstudianteDocente()
    #     esttudianteDocente=EstudianteDocente.objects.filter(id=expertoFicha.ficha.id)
    #     fichas_estudiantes.append(EstudianteDocente(esttudianteDocente))
    #

    return render(request, 'AppExperto/base.html',
                  {'notificaciones': notificaciones, 'fichas_estudiantes': fichas_estudiantes,
                   'usuario_logueado': usuario_logueado
                   })


# def estudianteFicha(request,cedula):
#     estudianteDocente= Estudian
#     estudianteRepresentante= EstudianteRepresentante.objects.get(cedula=cedula)
#
#     return render(request, 'AppExperto/verFichaEstudiante.html')


@login_required
def onesignal_register(request):
    experto = Experto.objects.get(user=request.user)  # The model where you will to save the profile.
    if request.POST.get('playerId'):
        experto.onesignal_playerId = request.POST.get('playerId')
        experto.save()
        return HttpResponse('Done')
    return HttpResponse('Something went wrong')


def visualizarCaso(request, cedula):
    global notificaciones
    usuarioLogueado = request.user
    estudianteDocenteFicha = None
    estudianteRepresentanteFicha = None


    if EstudianteRepresentante.objects.filter(cedula=cedula).exists():
        estudianteRepresentanteFicha = EstudianteRepresentante.objects.get(cedula=cedula)

    elif EstudianteDocente.objects.filter(cedula=cedula):
        estudianteDocenteFicha = EstudianteDocente.objects.get(cedula=cedula)

    comentarios = Comentario.objects.filter(fichaEstudiante_id=estudianteDocenteFicha.id).order_by('-id')

    # if request.method == 'POST':
    # comentario = Comentario()
    # comentario.contenido = request.POST['contenido']
    # comentario.emisor = request.user
    # comentario.receptor1 = request.POST['docenteReceptor']
    # comentario.receptor2 = request.POST['representanteReceptor']
    # comentario.save()
    return render(request, 'AppExperto/verFichaEstudiante.html',
                  {'estudianteDocenteFicha': estudianteDocenteFicha,
                   'estudianteRepresentanteFicha': estudianteRepresentanteFicha, 'notificaciones': notificaciones,
                   'usuarioLogueado': usuarioLogueado, 'comentarios': comentarios})


def vizualizarCasoActualizar(request):
    notificaciones = Notificacion.objects.filter(receptor_id=request.user.id)
    return HttpResponse(request, 'AppExperto/base.html', {'notificaciones': notificaciones})


@csrf_exempt
def crearComentario(request):
    comentarios = Comentario.objects.filter(fichaEstudiante_id=request.POST['id']).order_by('-id')

    print(request.POST['contenidoComentario'])

    # if request.is_ajax():
    if request.method == 'POST':
        # response_data = {}

        comentario = Comentario()
        comentario.contenido = request.POST['contenidoComentario']
        comentario.emisor = request.user
        fichaEstudiante = EstudianteDocente.objects.get(id=request.POST['id'])
        comentario.fichaEstudiante = fichaEstudiante
        comentario.correoEmisor = request.user.correo

        comentario.save()

        # response_data['contenido'] = request.POST['contenidoComentario']

        # for comenta in comentarios:
        #     comenta.emisor.correo
        data = serializers.serialize('json', comentarios)
        print(data)

        return HttpResponse(data, content_type='application/json')

    # return render(request, 'AppExperto/verFichaEstudiante.html',{'comentarios':comentarios})


def actualizarComentarios(request, id_estudiante):
    print(request.GET['fichaEstudianteId'])
