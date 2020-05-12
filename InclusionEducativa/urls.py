"""InclusionEducativa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import notifications.urls
from django.contrib import admin

from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView

from InclusionEducativa.Apps.GestionSistema.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^test/$', realizarTest, name='test'),
    url(r'^notificaciones/$', notificaciones, name='notificaciones'),
    url(r'^curriculum/$', curriculum, name='curriculum'),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('summernote/', include('django_summernote.urls')),
    url(r'^crearUsuario$', crearUsuario, name='crearUsuario'),
    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^accounts/logout/$', logout_view, name='logout'),
    url(r'^cambiar_password/', cambiarPassword, name='cambiar_password'),

    url(r'^appexperto/', include(('InclusionEducativa.Apps.AppExperto.urls', 'appexperto'), namespace='appexperto')),
    url(r'gestionsistema',
        include(('InclusionEducativa.Apps.GestionSistema.urls', 'gestionsistema'), namespace='gestionsistema')),
    url(r'^appdocente/', include(('InclusionEducativa.Apps.AppDocente.urls', 'appdocente'), namespace='appdocente')),
    url(r'^apprepresentante/',
        include(('InclusionEducativa.Apps.AppRepresentante.urls', 'apprepresentante'), namespace='apprepresentante')),

    path('chat/', include('django_chatter.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
