import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import get_default_password_validators, validate_password
from django.core.mail import send_mail, EmailMessage
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from notifications.models import Notification
from plainced import settings
from core.forms import *
from .models import *
from datetime import datetime, date
from notifications.signals import notify
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


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
        return redirect('gestionsistema:perfil')
    return render(request, 'core/perfil.html')


def verCurriculum(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    audio = textToSpeech(usuario)
    return render(request, 'core/verCurriculum.html', {'usuario': usuario, 'audio': audio})


def index(request):
    expertos = None
    if Experto.objects.all().exists():
        expertos = Experto.objects.all()
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        # Creamos el correo
        email = EmailMessage(
            subject,
            "De {} <{}>\n\nEscribió:\n\n{}".format(name, email, message),
            "no-contestar@ups.edu.ec",
            ["plainced@gmail.com"],
            reply_to=[email]
        )

        # Lo enviamos y redireccionamos
        try:
            email.send()
            # Todo ha ido bien, redireccionamos a OK
            return redirect(reverse('index') + "?ok")
        except:
            # Algo no ha ido bien, redireccionamos a FAIL
            return redirect(reverse('index') + "?fail")
    return render(request, 'core/index.html', {'expertos': expertos})


@login_required
def home(request):
    usuario_logueado = request.user
    usuarios = Usuario.objects.all().order_by('is_active', '-is_active')
    return render(request, 'core/home.html',
                  {'usuario_logueado': usuario_logueado, 'notificaciones': notificaciones, 'usuarios': usuarios})


def curriculum(request, usuario_id):
    experto = None
    if Experto.objects.filter(usuario_id=usuario_id).exists():
        experto = Experto.objects.get(usuario_id=usuario_id)
    return render(request, 'curriculum.html', {'experto': experto})


@login_required
def notificaciones(request):
    notificaciones = Notification.objects.filter(recipient_id=request.user.id).order_by('unread')
    data1 = serializers.serialize('json', notificaciones)
    return HttpResponse(data1, content_type='application/json')


def crearUsuario(request):
    instituciones = Institucion.objects.all()
    if request.method == 'POST':
        form_experto = ''
        form_docente = ''
        form_representante = ''
        if request.POST['tipo_usuario'] == 'experto':
            form_usuario = UsuarioForm(request.POST)
            form_experto = ExpertoForm(request.POST)
            if form_usuario.is_valid() and form_experto.is_valid():
                usuario = form_usuario.save(commit=False)
                usuario.is_active = False
                usuario.set_password(form_usuario.cleaned_data.get('password'))
                usuario.email = request.POST['username']
                messages.success(request,
                                 'Gracias por querer formar parte de nuestra plataforma, '
                                 'tu perfil está en revisión te avisaremos cuando culmine el proceso ')
                usuario.save()
                experto = form_experto.save(commit=False)
                experto.usuario = usuario
                experto.save()
                return redirect('gestionsistema:login')
        if request.POST['tipo_usuario'] == 'docente':
            form_usuario = UsuarioForm(request.POST)
            form_docente = DocenteForm(request.POST)
            if form_usuario.is_valid() and form_docente.is_valid():
                usuario = form_usuario.save(commit=False)
                usuario.is_active = True
                usuario.set_password(form_usuario.cleaned_data.get('password'))
                usuario.email = request.POST['username']
                messages.success(request, 'Cuenta creada con éxito puedes iniciar sesión')
                usuario.save()
                docente = form_docente.save(commit=False)
                docente.usuario = usuario
                docente.save()
                return redirect('gestionsistema:login')
        if request.POST['tipo_usuario'] == 'representante':
            form_usuario = UsuarioForm(request.POST)
            form_representante = RepresentanteForm(request.POST)
            if form_usuario.is_valid() and form_representante.is_valid():
                usuario = form_usuario.save(commit=False)
                usuario.is_active = True
                usuario.set_password(form_usuario.cleaned_data.get('password'))
                usuario.email = request.POST['username']
                messages.success(request, 'Cuenta creada con éxito puedes iniciar sesión')
                usuario.save()
                representante = form_representante.save(commit=False)
                representante.usuario = usuario
                representante.save()
                return redirect('gestionsistema:login')
                # experto = Experto()
                # experto.usuario = usuario
                # experto.tituloUniversitario = request.POST['tituloUniversitario']
                # experto.experienciaProfesional = request.POST['experienciaProfesional']
                # experto.save()
                # if usuario.tipo_usuario == 'representante':
                #     representante = Representante()
                #     representante.usuario = usuario
                #     representante.institucion = Institucion.objects.get(id=request.POST['institucion'])
                #     representante.save()
                # if usuario.tipo_usuario == 'docente':
                #     docente = Docente()
                #     docente.usuario = usuario
                #     docente.tituloUniversitario = request.POST['tituloUniversitario']
                #     docente.experienciaProfesional = request.POST['experienciaProfesional']
                #     docente.institucion = Institucion.objects.get(id=request.POST['institucion'])
                #     docente.save()
                # administradores = Usuario.objects.filter(tipo_usuario='Administrador')
                # sistema = Usuario.objects.get(username='jafetandres@hotmail.com')
                # notify.send(sistema, recipient=administradores, verb="/", description="Nuevo usuario registrado")
    else:
        form_usuario = UsuarioForm()
        form_experto = ExpertoForm()
        form_docente = DocenteForm()
        form_representante = RepresentanteForm()
    return render(request, 'core/registro.html',
                  {'form_usuario': form_usuario,
                   'form_experto': form_experto,
                   'form_docente': form_docente,
                   'form_representante': form_representante,
                   'instituciones': instituciones})


@login_required
def activarUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.is_active = True
    usuario.save()
    return redirect('gestionsistema:home')


@login_required
def desactivarUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.is_active = False
    usuario.save()
    return redirect('gestionsistema:home')


@login_required
def cambiarContrasena(request):
    errores = []
    bandera = False
    if request.method == 'POST':
        if request.user.check_password(request.POST['old_password']) is False:
            errores.append("La contraseña anterior es incorrecta")
            bandera = False
        else:
            bandera = True
        if len(request.POST['new_password2']) < 8:
            errores.append("La nueva contraseña debe tener minimo 8 caracteres")
            bandera = False
        else:
            bandera = True
        indice = 0
        mayusculas = 0
        minusculas = 0
        while indice < len(request.POST['new_password2']):
            letra = request.POST['new_password2'][indice]
            if letra.isupper() == True:
                mayusculas += 1
            else:
                minusculas += 1
            indice += 1
        if mayusculas < 1:
            errores.append("La nueva contraseña debe tener minimo una letra en mayuscula")
            bandera = False
        else:
            bandera = True
        if minusculas < 1:
            errores.append("La nueva contraseña debe tener minimo una letra en minuscula")
            bandera = False
        else:
            bandera = True
        if request.POST['new_password1'] != request.POST['new_password2']:
            errores.append("La nueva contraseña no coicide con la confirmacion")
            bandera = False
        else:
            bandera = True
        if bandera is True:
            usuario = Usuario.objects.get(id=request.user.id)
            usuario.set_password(request.POST['new_password2'])
            usuario.save()
            login(request, usuario)

    json_dump = json.dumps(errores)
    return HttpResponse(json_dump, content_type='application/json')


def InstitucionCrear(request):
    usuario_logueado = request.user
    password_validators = get_default_password_validators()
    if request.method == 'POST':
        form = InstitucionForm(request.POST)
        if form.is_valid():
            form.save()
            notify.send(request.user, recipient=request.user, verb="/")
        return redirect('gestionsistema:institucion_listar')
    else:
        form = InstitucionForm()
    return render(request, 'core/institucion_crear.html',
                  {'form': form, 'usuario_logueado': usuario_logueado})


def InstitucionListar(request):
    usuario_logueado = request.user
    institucion = Institucion.objects.all()

    return render(request, 'core/institucion_listar.html',
                  {'instituciones': institucion, 'usuario_logueado': usuario_logueado})


def InstitucionEditar(request, id_institucion):
    usuario_logueado = request.user
    institucion = Institucion.objects.get(id=id_institucion)
    if request.method == 'POST':
        form = InstitucionForm(request.POST, instance=institucion)
        if form.is_valid():
            form.save()
        return redirect('gestionsistema:institucion_listar')
    return render(request, 'core/institucion_crear.html',
                  {'form_institucion': institucion, 'usuario_logueado': usuario_logueado})


def InstitucionEliminar(request, id_institucion):
    usuario_logueado = request.user
    institucion = Institucion.objects.get(id=id_institucion)
    if request.method == 'POST':
        institucion.delete()
        return redirect('gestionsistema:institucion_listar')
    return render(request, 'core/institucion_eliminar.html',
                  {'institucion': institucion, 'usuario_logueado': usuario_logueado})


def ExpertoCrear(request):
    usuario_logueado = request.user
    instituciones = Institucion.objects.all()
    if request.method == 'POST':
        form_usuario = UsuarioForm(request.POST)
        form_experto = ExpertoForm(request.POST)
        if form_experto.is_valid() and form_usuario.is_valid():
            usuario = form_usuario.save(commit=False)
            password_generate = get_random_string(length=8)
            usuario.set_password(password_generate)
            usuario.tipo_user = 'Experto'
            form_usuario.save()
            experto = form_experto.save(commit=False)
            experto.foto = request.FILES.get('foto')
            experto.usuario = form_usuario.instance
            form_experto.save()
            usuarioChat = UserProfile()
            usuarioChat.user = usuario
            usuarioChat.last_visit = datetime.now()
            usuarioChat.save()

            contenido = 'Hola bienvenido a Inclusion educativa tu para ingresar al sistema utiliza los siguiente datos Correo: ' + usuario.__str__() + 'Contraseña: ' + password_generate
            res = send_mail("Creacion de Usuario Inclusion Educativa", contenido, settings.EMAIL_HOST_USER,
                            [usuario.__str__()])
        return redirect('gestionsistema:experto_listar')
    else:
        form_usuario = UsuarioForm()
        form_experto = Experto()
    return render(request, 'core/experto_crear.html', {'form_usuario': form_usuario,
                                                       'form_experto': form_experto,
                                                       'instituciones': instituciones,
                                                       'usuario_logueado': usuario_logueado})


def ExpertoListar(request):
    usuario_logueado = request.user
    expertos = Experto.objects.all()

    return render(request, 'core/experto_listar.html',
                  {'usuario_logueado': usuario_logueado, 'expertos': expertos})


def ExpertoEditar(request, id_experto):
    usuario_logueado = request.user
    experto = Experto.objects.get(id=id_experto)
    usuario = Usuario.objects.get(id=experto.usuario.id)
    if request.method == 'POST':
        # contrasena_anterior = ''
        # bandera = True
        # if request.POST['password'] == '':
        #     bandera = False
        #     contrasena_anterior = experto.usuario.password
        # else:
        #     contrasena_anterior = request.POST['password']
        # request.POST._mutable = True
        # request.POST['password'] = contrasena_anterior
        # request.POST['repeat_password'] = contrasena_anterior
        # request.POST._mutable = False
        form_experto = ExpertoForm(request.POST, instance=experto)
        form_usuario = UsuarioForm(request.POST, instance=usuario)
        if form_experto.is_valid() and form_usuario.is_valid():
            usu = form_usuario.save(commit=False)
            # if bandera:
            #     usu.set_password(contrasena_anterior)
            usu.save()
            doc = form_experto.save(commit=False)
            doc.usuario = usu
            doc.save()
        return redirect('gestionsistema:experto_listar')
    return render(request, 'core/experto_crear.html',
                  {'form_experto': experto, 'usuario_logueado': usuario_logueado})


def ExpertoEliminar(request, id_experto):
    usuario_logueado = request.user
    experto = Experto.objects.get(id=id_experto)
    usuario = Usuario.objects.get(id=experto.usuario.id)
    if request.method == 'POST':
        experto.delete()
        usuario.delete()
        return redirect('gestionsistema:experto_listar')
    return render(request, 'core/experto_eliminar.html',
                  {'experto': experto, 'usuario_logueado': usuario_logueado})


def DocenteCrear(request):
    usuario_logueado = request.user
    instituciones = Institucion.objects.all()
    if request.method == 'POST':
        form_usuario = UsuarioForm(request.POST)
        form_docente = DocenteForm(request.POST)
        if form_docente.is_valid() and form_usuario.is_valid():
            usuario = form_usuario.save(commit=False)
            password_generate = get_random_string(length=8)
            usuario.set_password(password_generate)
            usuario.tipo_user = 'Docente'
            form_usuario.save()
            docente = form_docente.save(commit=False)
            docente.usuario = form_usuario.instance
            form_docente.save()
            contenido = 'Hola bienvenido a Inclusion educativa tu para ingresar al sistema utiliza los siguiente datos Correo: ' + usuario.__str__() + 'Contraseña: ' + password_generate
            res = send_mail("Creacion de Usuario Inclusion Educativa", contenido, settings.EMAIL_HOST_USER,
                            [usuario.__str__()])
        return redirect('gestionsistema:docente_listar')
    else:
        form_usuario = UsuarioForm()
        form_docente = Docente()
    return render(request, 'core/docente_crear.html', {'form_usuario': form_usuario,
                                                       'form_docente': form_docente,
                                                       'instituciones': instituciones,
                                                       'usuario_logueado': usuario_logueado})


def DocenteListar(request):
    usuario_logueado = request.user
    docentes = Docente.objects.all()

    return render(request, 'core/docente_listar.html',
                  {'usuario_logueado': usuario_logueado, 'docentes': docentes})


def DocenteEditar(request, id_docente):
    usuario_logueado = request.user
    docente = Docente.objects.get(id=id_docente)
    usuario = Usuario.objects.get(id=docente.usuario.id)
    instituciones = Institucion.objects.all()
    if request.method == 'POST':
        form_docente = DocenteForm(request.POST, instance=docente)
        form_usuario = UsuarioForm(request.POST, instance=usuario)
        if form_docente.is_valid() and form_usuario.is_valid():
            usu = form_usuario.save(commit=False)
            usu.save()
            doc = form_docente.save(commit=False)
            doc.usuario = usu
            doc.save()
        return redirect('gestionsistema:docente_listar')
    return render(request, 'core/docente_crear.html', {'form_docente': docente,
                                                       'instituciones': instituciones,
                                                       'usuario_logueado': usuario_logueado})


def DocenteEliminar(request, id_docente):
    usuario_logueado = request.user
    docente = Docente.objects.get(id=id_docente)
    usuario = Usuario.objects.get(id=docente.usuario.id)
    if request.method == 'POST':
        docente.delete()
        usuario.delete()
        return redirect('gestionsistema:docente_listar')
    return render(request, 'core/docente_eliminar.html',
                  {'docente': docente, 'usuario_logueado': usuario_logueado})


def representanteCrear(request):
    usuario_logueado = request.user
    instituciones = Institucion.objects.all()
    form_representante = None
    form_usuario = None
    if request.method == 'POST':
        form_usuario = UsuarioForm(request.POST)
        form_representante = RepresentanteForm(request.POST)
        if form_representante.is_valid() and form_usuario.is_valid():
            usuario = form_usuario.save(commit=False)
            password_generate = get_random_string(length=8)
            usuario.set_password(password_generate)
            usuario.tipo_user = 'Representante'
            form_usuario.save()
            representante = form_representante.save(commit=False)
            representante.usuario = form_usuario.instance

            form_representante.save()
            contenido = 'Hola bienvenido a Inclusion educativa tu para ingresar al sistema utiliza los siguiente datos Correo: ' + usuario.__str__() + 'Contraseña: ' + password_generate
            res = send_mail("Creacion de Usuario Inclusion Educativa", contenido, settings.EMAIL_HOST_USER,
                            [usuario.__str__()])

        return redirect('gestionsistema:representante_listar')

    return render(request, 'core/representante_crear.html', {
        'form_representante': form_representante,
        'form_usuario': form_usuario,
        'instituciones': instituciones,
        'usuario_logueado': usuario_logueado})


def RepresentanteListar(request):
    usuario_logueado = request.user
    representantes = Representante.objects.all()

    return render(request, 'core/representante_listar.html',
                  {'usuario_logueado': usuario_logueado, 'representantes': representantes})


def RepresentanteEditar(request, id_representante):
    usuario_logueado = request.user
    representante = Representante.objects.get(id=id_representante)
    usuario = Usuario.objects.get(id=representante.usuario.id)
    instituciones = Institucion.objects.all()
    if request.method == 'POST':
        form_representante = RepresentanteForm(request.POST, instance=representante)
        form_usuario = UsuarioForm(request.POST, instance=usuario)
        if form_representante.is_valid() and form_usuario.is_valid():
            usu = form_usuario.save(commit=False)
            usu.save()
            doc = form_representante.save(commit=False)
            doc.usuario = usu
            doc.save()
        return redirect('gestionsistema:representante_listar')
    return render(request, 'core/representante_crear.html', {'form_representante': representante,
                                                             'instituciones': instituciones,
                                                             'usuario_logueado': usuario_logueado})


def RepresentanteEliminar(request, id_representante):
    usuario_logueado = request.user
    representante = Representante.objects.get(id=id_representante)
    usuario = Usuario.objects.get(id=representante.usuario.id)
    if request.method == 'POST':
        representante.delete()
        usuario.delete()
        return redirect('gestionsistema:representante_listar')
    return render(request, 'core/representante_eliminar.html',
                  {'representante': representante, 'usuario_logueado': usuario_logueado})


def logout_view(request):
    usuario = Usuario.objects.get(id=request.user.id)
    usuario.is_online = False
    usuario.save()
    logout(request)
    return redirect('index')


def buscarUsuario(request):
    if 'cedula' in request.GET:
        if Usuario.objects.filter(cedula=request.GET['cedula']).exists():
            usuario1 = Usuario.objects.filter(cedula=request.GET['cedula'])
            data1 = serializers.serialize('json', usuario1)
            return HttpResponse(data1, content_type='application/json')

    if 'username' in request.GET:
        if Usuario.objects.filter(username=request.GET['username']).exists():
            usuario2 = Usuario.objects.filter(username=request.GET['username'])
            data2 = serializers.serialize('json', usuario2)
            return HttpResponse(data2, content_type='application/json')


def reenviarContrasena(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    password_generate = get_random_string(length=8)
    usuario.set_password(password_generate)
    contenido = 'Hola bienvenido a Inclusion educativa tu para ingresar al sistema utiliza los siguiente datos Correo: ' + usuario.__str__() + 'Contraseña: ' + password_generate
    res = send_mail("Creacion de Usuario Inclusion Educativa", contenido, settings.EMAIL_HOST_USER,
                    [usuario.__str__()])


@csrf_exempt
@login_required
def crearComentario(request):
    if request.method == 'POST':
        comentario = Comentario()
        comentario.contenido = request.POST['contenidoComentario']
        comentario.emisor = request.user
        estudiante = Estudiante.objects.get(id=request.POST['id'])
        comentario.estudiante = estudiante
        comentario.receptor = request.POST.get('receptor', False)
        comentario.save()
        # receptores = []
        # representante = FichaInformativaRepresentante.objects.get(estudiante_id=estudiante.id).representante.usuario
        # receptores.append(representante)
        # docente = FichaInformativaDocente.objects.get(estudiante_id=estudiante.id).docente.usuario
        # receptores.append(docente)
        # verbDocente = "/appdocente/verFichaInformativa/" + estudiante.cedula
        # descripcion = "Nuevo comentario de " + request.user.nombres + " para " + estudiante.nombres + " " + estudiante.apellidos
        # verbRepresente = "/apprepresentante/verFichaInformativa/" + estudiante.cedula
        # notify.send(request.user, recipient=docente, actor=request.user,
        #             verb=verbDocente,
        #             description=descripcion, target=estudiante)
        # notify.send(request.user, recipient=representante, actor=request.user,
        #             verb=verbRepresente,
        #             description=descripcion, target=estudiante)


@login_required
def cargarComentarios(request):
    comentarios = Comentario.objects.filter(estudiante_id=request.GET['id']).order_by('-timestamp')
    lista = []
    for comentario in comentarios:
        foto = 'https://image.ibb.co/jw55Ex/def_face.jpg'
        if comentario.emisor.foto:
            foto = comentario.emisor.foto.url
        lista.append({'nombre': comentario.emisor.nombres,
                      'foto': foto,
                      'contenido': comentario.contenido})
    return JsonResponse({"message": "success",
                         'comentarios': lista
                         }, safe=False)


@login_required
def cargarComentariosDocente(request):
    comentariosAll = Comentario.objects.filter(estudiante_id=request.GET['id'],
                                               receptor='docente').order_by('-timestamp')
    comentarios = []
    for comentario in comentariosAll:
        if comentario.emisor.tipo_usuario == 'docente' or comentario.emisor.tipo_usuario == 'experto':
            comentarios.append(comentario)

    lista = []
    for comentario in comentarios:
        foto = 'https://image.ibb.co/jw55Ex/def_face.jpg'
        if comentario.emisor.foto:
            foto = comentario.emisor.foto.url
        lista.append({'nombre': comentario.emisor.nombres,
                      'foto': foto,
                      'contenido': comentario.contenido})
    return JsonResponse({"message": "success",
                         'comentarios': lista
                         }, safe=False)


@login_required
def cargarComentariosRepresentante(request):
    comentariosAll = Comentario.objects.filter(estudiante_id=request.GET['id'],
                                               receptor='representante').order_by('-timestamp')
    comentarios = []
    for comentario in comentariosAll:
        if comentario.emisor.tipo_usuario == 'representante' or comentario.emisor.tipo_usuario == 'experto':
            comentarios.append(comentario)

    lista = []
    for comentario in comentarios:
        foto = 'https://image.ibb.co/jw55Ex/def_face.jpg'
        if comentario.emisor.foto:
            foto = comentario.emisor.foto.url
        lista.append({'nombre': comentario.emisor.nombres,
                      'foto': foto,
                      'contenido': comentario.contenido})
    return JsonResponse({"message": "success",
                         'comentarios': lista
                         }, safe=False)
