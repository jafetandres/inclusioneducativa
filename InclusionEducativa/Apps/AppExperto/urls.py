from django.urls import path
from django.conf.urls import url, include

from InclusionEducativa.Apps.AppExperto.views import *

urlpatterns = [
    url(r'^$', base, name='base'),
    url(r'^visualizarCaso/(?P<cedula>\d+)/$', visualizarCaso, name='visualizarCaso'),
    url(r'^refrescanotificacion$', vizualizarCasoActualizar, name='refrescanotificacion'),
    url(r'^crearComentario/$', crearComentario, name='crearComentario'),
    url(r'^perfil/$', perfil, name='perfil'),

    path('onesignal_register/', onesignal_register, name='onesignal_register'),
    url(r'^actualizarComentarios$',actualizarComentarios,name='actualizarComentarios'),
  

]
