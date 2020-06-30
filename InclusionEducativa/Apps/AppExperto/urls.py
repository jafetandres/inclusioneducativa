from django.urls import path
from django.conf.urls import url, include
from InclusionEducativa.Apps.AppExperto.views import *

app_name = 'appexperto'
urlpatterns = [
    url(r'^$', base, name='base'),
    url(r'^verFicha/(?P<cedula>\d+)/$', verFicha, name='verFicha'),
    url(r'^crearComentario/$', crearComentario, name='crearComentario'),
    url(r'^perfil/(?P<id_usuario>\d+)/$', perfil, name='perfil'),
    path('onesignal_register/', onesignal_register, name='onesignal_register'),

]
