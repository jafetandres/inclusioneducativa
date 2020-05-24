from django.conf.urls import url
from InclusionEducativa.Apps.AppDocente.views import *

urlpatterns = [
    url(r'^$', base, name='base'),
    url(r'^comentarios$', comentarios, name='comentarios'),
    url(r'^buscarEstudiante$', buscarEstudiante, name='buscarEstudiante'),
    url(r'^verFichaInformativa/(?P<cedula>\d+)/$', verFichaInformativa, name='verFichaInformativa'),
    url(r'^perfil$', perfil, name='perfil'),
    url(r'^crearFichaInformativa/(?P<estudiante_cedula>\d+)/$', crearFichaInformativa, name='crearFichaInformativa'),
    # url(r'^estudiante_test$', EstudianteTest, name='estudiante_test'),
    # url(r'^resultado_test$', ResultadoTest, name='resultado_test'),
]
