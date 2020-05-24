from InclusionEducativa.Apps.GestionSistema.views import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', base, name='base'),
    url(r'^activarUsuario/(?P<id_usuario>\d+)/$', login_required(activarUsuario), name='activarUsuario'),
    url(r'^desactivarUsuario/(?P<id_usuario>\d+)/$', login_required(desactivarUsuario), name='desactivarUsuario'),
    url(r'^institucion_listar$', login_required(InstitucionListar), name='institucion_listar'),
    url(r'^institucion_crear$', login_required(InstitucionCrear), name='institucion_crear'),
    url(r'^institucion_editar/(?P<id_institucion>\d+)/$', login_required(InstitucionEditar), name='institucion_editar'),
    url(r'^institucion_eliminar/(?P<id_institucion>\d+)/$', login_required(InstitucionEliminar),
        name='institucion_eliminar'),
    url(r'^experto_listar$', login_required(ExpertoListar), name='experto_listar'),
    url(r'^experto_crear$', login_required(ExpertoCrear), name='experto_crear'),
    url(r'^experto_editar/(?P<id_experto>\d+)/$', login_required(ExpertoEditar), name='experto_editar'),
    url(r'^experto_eliminar/(?P<id_experto>\d+)/$', login_required(ExpertoEliminar), name='experto_eliminar'),
    url(r'^docente_listar$', login_required(DocenteListar), name='docente_listar'),
    url(r'^docente_crear$', DocenteCrear, name='docente_crear'),
    url(r'^docente_editar/(?P<id_docente>\d+)/$', login_required(DocenteEditar), name='docente_editar'),
    url(r'^docente_eliminar/(?P<id_docente>\d+)/$', login_required(DocenteEliminar), name='docente_eliminar'),
    url(r'^representante_listar$', RepresentanteListar, name='representante_listar'),
    url(r'^representante_crear$', representanteCrear, name='representante_crear'),
    url(r'^representante_editar/(?P<id_representante>\d+)/$', login_required(RepresentanteEditar),
        name='representante_editar'),
    url(r'^representante_eliminar/(?P<id_representante>\d+)/$', login_required(RepresentanteEliminar),
        name='representante_eliminar'),
    url(r'^perfil', login_required(perfil), name='perfil'),
    url(r'^buscarUsuario$', buscarUsuario,
        name='buscarUsuario'),
    url(r'^verCurriculum/(?P<usuario_id>\d+)/$', verCurriculum,
        name='verCurriculum'),

]
