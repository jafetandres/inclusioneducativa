from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from core.models import Usuario


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
                        return redirect('appdocente:home')
                    elif user.tipo_usuario == 'experto':
                        return redirect('appexperto:base')
                    elif user.tipo_usuario == 'representante':
                        return redirect('apprepresentante:base')
                    elif user.tipo_usuario == 'administrador' and user.is_superuser:
                        return redirect('core:home')
                else:
                    messages.error(request, 'Correo electronico o contraseña incorrectos')
            else:
                messages.error(request, 'El usuario esta desactivado')
        else:
            messages.error(request, 'El usuario no existe')
    return render(request, 'registration/login.html')
