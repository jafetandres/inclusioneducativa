from django.conf.urls import url
from django.urls import path

from docente.views import *

app_name = 'appdocente'
urlpatterns = [
    path('', home, name='home'),
    path('editarFichaInformativa/<int:estudiante_id>/', editarFichaInformativa, name='editarFichaInformativa'),
    url(r'^comentarios$', comentarios, name='comentarios'),
    path('buscarEstudiante/', buscarEstudiante, name='buscarEstudiante'),
    url(r'^verFichaInformativa/(?P<cedula>\d+)/$', verFichaInformativa, name='verFichaInformativa'),
    url(r'^perfil$', perfil, name='perfil'),
    url(r'^crearFichaInformativa/(?P<estudiante_cedula>\d+)/$', crearFichaInformativa, name='crearFichaInformativa'),
    # url(r'^estudiante_test$', EstudianteTest, name='estudiante_test'),
    # url(r'^resultado_test$', ResultadoTest, name='resultado_test'),
]
