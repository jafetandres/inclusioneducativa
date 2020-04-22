from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from InclusionEducativa.Apps.AppDocente.views import *

urlpatterns = [
    url(r'^$', base, name='base'),
    url(r'^perfil/(?P<id_usuario>\d+)/$', login_required(perfil), name='perfil'),
    url(r'^fichaEstudianteCrear$', fichaEstudianteCrear, name='fichaEstudianteCrear'),
    url(r'^estudiante_test$', EstudianteTest, name='estudiante_test'),
    url(r'^resultado_test$', ResultadoTest, name='resultado_test'),
    url(r'^fichaEstudianteListar$', fichaEstudianteListar, name='fichaEstudianteListar'),
    url(r'^estudiante_editar/(?P<id_estudiante>\d+)/$', EstudianteEditar, name='estudiante_editar'),
    url(r'^estudiante_eliminar/(?P<id_estudiante>\d+)/$', EstudianteEliminar, name='estudiante_eliminar'),
]
