from django.conf.urls import url

from InclusionEducativa.Apps.AppRepresentante.views import *

urlpatterns = [
    url(r'^$', base, name='base'),
    url(r'^buscarEstudiante$', buscarEstudiante, name='buscarEstudiante'),
    url(r'^perfil$', perfil, name='perfil'),
    url(r'^crearFichaInformativa/(?P<estudiante_cedula>\d+)/$', crearFichaInformativa, name='crearFichaInformativa'),
    url(r'^verFichaInformativa/(?P<cedula>\d+)/$', verFichaInformativa, name='verFichaInformativa'),

]
