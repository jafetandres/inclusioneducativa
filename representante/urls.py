from django.conf.urls import url
from django.urls import path

from representante.views import *

app_name = 'apprepresentante'
urlpatterns = [
    path('', home, name='home'),
    url(r'^buscarEstudiante$', buscarEstudiante, name='buscarEstudiante'),
    path('editarFichaInformativa/<int:estudiante_id>/', editarFichaInformativa, name='editarFichaInformativa'),
    path('perfil/', perfil, name='perfil'),
    url(r'^crearFichaInformativa/(?P<estudiante_cedula>\d+)/$', crearFichaInformativa, name='crearFichaInformativa'),
    url(r'^verFichaInformativa/(?P<cedula>\d+)/$', verFichaInformativa, name='verFichaInformativa'),

]
