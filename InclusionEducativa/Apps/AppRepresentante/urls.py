from django.conf.urls import url
from django.urls import path

from InclusionEducativa.Apps.AppRepresentante.views import *

app_name = 'apprepresentante'
urlpatterns = [
    url(r'^$', base, name='base'),
    url(r'^buscarEstudiante$', buscarEstudiante, name='buscarEstudiante'),
    path('perfil/', perfil, name='perfil'),
    url(r'^crearFichaInformativa/(?P<estudiante_cedula>\d+)/$', crearFichaInformativa, name='crearFichaInformativa'),
    url(r'^verFichaInformativa/(?P<cedula>\d+)/$', verFichaInformativa, name='verFichaInformativa'),

]
