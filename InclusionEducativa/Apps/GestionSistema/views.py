from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, views

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from InclusionEducativa import settings
from InclusionEducativa.Apps.GestionSistema.forms import *
from InclusionEducativa.Apps.GestionSistema.models import *
from django_chatter.models import UserProfile
from datetime import datetime
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')


def base(request):
    usuario_logueado = request.user
    return render(request, 'GestionSistema/base.html', {'usuario_logueado': usuario_logueado})

def curriculum(request):

    return render(request, 'curriculum.html')



def cambiarPassword(request):
    if request.method == 'POST':
        usuario = Usuario.objects.get(id=request.user.id)
        nuevo_password = request.POST['password']
        usuario.set_password(nuevo_password)
        usuario.save()
        logout(request.user)
        return redirect('login')
    return render(request, "cambiar_password.html")


def InstitucionCrear(request):
    usuario_logueado = request.user
    if request.method == 'POST':
        form = InstitucionForm(request.POST)
        if form.is_valid():
            form.save()
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
            experto.foto=request.FILES.get('foto')
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
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = request.POST['correo']
            password = request.POST['password']
            user = authenticate(correo=correo, password=password)
            if user is not None:
                login(request, user)

                if user.tipo_user == 'Docente':
                    return redirect('appdocente:base')
                elif user.tipo_user == 'Experto':
                    return redirect('appexperto:base')
                elif user.tipo_user == 'Representante':
                    return redirect('apprepresentante:base')
                return redirect('gestionsistema:base')
            else:
                form = LoginForm()
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def perfil(request, id_usuario):
    usuario_logueado = request.user
    usuario = Usuario.objects.get(id=request.user.id)
    form_usuario = UsuarioForm(request.POST, instance=usuario)
    if request.method == 'POST':
        if form_usuario.is_valid():
            form_usuario.save()

        return redirect('gestionsistema:base')
    return render(request, 'GestionSistema/perfil.html', {'usuario': usuario,
                                                          'usuario_logueado': usuario_logueado})


def buscarUsuario(request):
    if 'cedula' in request.GET:
        if Usuario.objects.filter(cedula=request.GET['cedula']).exists():
            usuario1 = Usuario.objects.filter(cedula=request.GET['cedula'])
            data1 = serializers.serialize('json', usuario1)
            return HttpResponse(data1, content_type='application/json')

    if 'correo' in request.GET:
        if Usuario.objects.filter(correo=request.GET['correo']).exists():
            usuario2 = Usuario.objects.filter(correo=request.GET['correo'])
            data2 = serializers.serialize('json', usuario2)
            return HttpResponse(data2, content_type='application/json')


def reenviarContrasena(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    password_generate = get_random_string(length=8)
    usuario.set_password(password_generate)
    contenido = 'Hola bienvenido a Inclusion educativa tu para ingresar al sistema utiliza los siguiente datos Correo: ' + usuario.__str__() + 'Contraseña: ' + password_generate
    res = send_mail("Creacion de Usuario Inclusion Educativa", contenido, settings.EMAIL_HOST_USER,
                    [usuario.__str__()])
