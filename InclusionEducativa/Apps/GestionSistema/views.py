import json
import io
from django.contrib import messages, staticfiles
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from notifications.models import Notification
from InclusionEducativa import settings
from InclusionEducativa.Apps.GestionSistema.forms import *
from InclusionEducativa.Apps.GestionSistema.models import *
from django_chatter.models import UserProfile
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
    return render(request, 'GestionSistema/perfil.html')


def verCurriculum(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    return render(request, 'GestionSistema/verCurriculum.html', {'usuario': usuario})


def index(request):
    usuario_logueado = None
    if request.user.is_authenticated:
        usuario_logueado = Usuario.objects.get(id=request.user.id)
    return render(request, 'index.html', {'usuario_logueado': usuario_logueado})


@login_required
def base(request):
    usuario_logueado = request.user

    usuarios = Usuario.objects.all().order_by('is_active', '-is_active')
    return render(request, 'GestionSistema/base.html',
                  {'usuario_logueado': usuario_logueado, 'notificaciones': notificaciones, 'usuarios': usuarios})


def curriculum(request):
    return render(request, 'curriculum.html')


@login_required
def notificaciones(request):
    notificaciones = Notification.objects.filter(recipient_id=request.user.id).order_by('unread')
    data1 = serializers.serialize('json', notificaciones)
    return HttpResponse(data1, content_type='application/json')


def crearUsuario(request):
    instituciones = Institucion.objects.all()
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            if request.POST['password'] == request.POST['password2']:
                usuario = form.save()
                usuario.is_active = True
                usuario.set_password(form.cleaned_data.get('password'))
                usuario.email = request.POST['username']
                usuario.save()
                if usuario.tipo_usuario == 'experto':
                    experto = Experto()
                    experto.usuario = usuario
                    experto.save()
                if usuario.tipo_usuario == 'representante':
                    representante = Representante()
                    representante.usuario = usuario
                    representante.save()
                if usuario.tipo_usuario == 'docente':
                    docente = Docente()
                    docente.usuario = usuario
                    docente.save()
                administradores = Usuario.objects.filter(tipo_usuario='Administrador')
                sistema = Usuario.objects.get(username='jafetandres@hotmail.com')
                notify.send(sistema, recipient=administradores, verb="/", description="Nuevo usuario registrado")
                messages.info(request, 'Cuenta creada con exito inicia sesion')
                return redirect('login')
            else:
                messages.error(request, 'Verifique que todos los campos esten correctos.')
    else:
        form = UsuarioForm()
    return render(request, 'registro.html', {'form': form, 'instituciones': instituciones})


@login_required
def activarUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.is_active = True
    usuario.save()
    return redirect('gestionsistema:base')


@login_required
def desactivarUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.is_active = False
    usuario.save()
    return redirect('gestionsistema:base')


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
    return render(request, 'GestionSistema/institucion_crear.html',
                  {'form': form, 'usuario_logueado': usuario_logueado})


def InstitucionListar(request):
    usuario_logueado = request.user
    institucion = Institucion.objects.all()

    return render(request, 'GestionSistema/institucion_listar.html',
                  {'instituciones': institucion, 'usuario_logueado': usuario_logueado})


def InstitucionEditar(request, id_institucion):
    usuario_logueado = request.user
    institucion = Institucion.objects.get(id=id_institucion)
    if request.method == 'POST':
        form = InstitucionForm(request.POST, instance=institucion)
        if form.is_valid():
            form.save()
        return redirect('gestionsistema:institucion_listar')
    return render(request, 'GestionSistema/institucion_crear.html',
                  {'form_institucion': institucion, 'usuario_logueado': usuario_logueado})


def InstitucionEliminar(request, id_institucion):
    usuario_logueado = request.user
    institucion = Institucion.objects.get(id=id_institucion)
    if request.method == 'POST':
        institucion.delete()
        return redirect('gestionsistema:institucion_listar')
    return render(request, 'GestionSistema/institucion_eliminar.html',
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
    return render(request, 'GestionSistema/experto_crear.html', {'form_usuario': form_usuario,
                                                                 'form_experto': form_experto,
                                                                 'instituciones': instituciones,
                                                                 'usuario_logueado': usuario_logueado})


def ExpertoListar(request):
    usuario_logueado = request.user
    expertos = Experto.objects.all()

    return render(request, 'GestionSistema/experto_listar.html',
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
    return render(request, 'GestionSistema/experto_crear.html',
                  {'form_experto': experto, 'usuario_logueado': usuario_logueado})


def ExpertoEliminar(request, id_experto):
    usuario_logueado = request.user
    experto = Experto.objects.get(id=id_experto)
    usuario = Usuario.objects.get(id=experto.usuario.id)
    if request.method == 'POST':
        experto.delete()
        usuario.delete()
        return redirect('gestionsistema:experto_listar')
    return render(request, 'GestionSistema/experto_eliminar.html',
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
    return render(request, 'GestionSistema/docente_crear.html', {'form_usuario': form_usuario,
                                                                 'form_docente': form_docente,
                                                                 'instituciones': instituciones,
                                                                 'usuario_logueado': usuario_logueado})


def DocenteListar(request):
    usuario_logueado = request.user
    docentes = Docente.objects.all()

    return render(request, 'GestionSistema/docente_listar.html',
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
    return render(request, 'GestionSistema/docente_crear.html', {'form_docente': docente,
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
    return render(request, 'GestionSistema/docente_eliminar.html',
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

    return render(request, 'GestionSistema/representante_crear.html', {
        'form_representante': form_representante,
        'form_usuario': form_usuario,
        'instituciones': instituciones,
        'usuario_logueado': usuario_logueado})


def RepresentanteListar(request):
    usuario_logueado = request.user
    representantes = Representante.objects.all()

    return render(request, 'GestionSistema/representante_listar.html',
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
    return render(request, 'GestionSistema/representante_crear.html', {'form_representante': representante,
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
    return render(request, 'GestionSistema/representante_eliminar.html',
                  {'representante': representante, 'usuario_logueado': usuario_logueado})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if Usuario.objects.filter(username=username).exists():
            usuario = Usuario.objects.get(username=username)
            if usuario.is_active:
                if user is not None:
                    login(request, user)
                    usuario.is_online = True
                    usuario.save()
                    if user.tipo_usuario == 'docente':
                        return redirect('appdocente:base')
                    elif user.tipo_usuario == 'experto':
                        return redirect('appexperto:base')
                    elif user.tipo_usuario == 'representante':
                        return redirect('apprepresentante:base')
                    else:
                        return redirect('gestionsistema:base')
                else:
                    messages.error(request, 'Correo electronico o contraseña incorrectos')
            else:
                messages.error(request, 'El usuario esta desactivado')
        else:
            messages.error(request, 'El usuario no existe')
    return render(request, 'login.html')


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

