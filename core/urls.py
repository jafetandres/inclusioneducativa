from django.urls import path
from core.views import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

app_name = 'gestionsistema'

urlpatterns = [
    path('', base, name='base'),
    path('crearComentario/', crearComentario, name='crearComentario'),
    path('cargarComentarios/', cargarComentarios, name='cargarComentarios'),
    path('cargarComentariosDocente/', cargarComentariosDocente, name='cargarComentariosDocente'),
    path('cargarComentariosRepresentante/', cargarComentariosRepresentante, name='cargarComentariosRepresentante'),
    path('curriculum/<usuario_id>/', curriculum, name='curriculum'),
    path('crearUsuario/', crearUsuario, name='crearUsuario'),
    path('login/', login_view, name='login'),
    path('notificaciones/', notificaciones, name='notificaciones'),
    path('cambiarContrasena/', cambiarContrasena, name='cambiarContrasena'),
    path('logout/', logout_view, name='logout'),
    url(r'^activarUsuario/(?P<id_usuario>\d+)/$', activarUsuario, name='activarUsuario'),
    url(r'^desactivarUsuario/(?P<id_usuario>\d+)/$', desactivarUsuario, name='desactivarUsuario'),
    path('institucion_listar/', InstitucionListar, name='institucion_listar'),
    path('institucion_crear/', InstitucionCrear, name='institucion_crear'),
    url(r'^institucion_editar/(?P<id_institucion>\d+)/$', InstitucionEditar, name='institucion_editar'),
    url(r'^institucion_eliminar/(?P<id_institucion>\d+)/$', InstitucionEliminar,
        name='institucion_eliminar'),
    path('perfil/', perfil, name='perfil'),
    url(r'^buscarUsuario$', buscarUsuario,
        name='buscarUsuario'),
    url(r'^verCurriculum/(?P<usuario_id>\d+)/$', verCurriculum,
        name='verCurriculum'),

]

# url(r'^experto_listar$', login_required(ExpertoListar), name='experto_listar'),
# url(r'^experto_crear$', login_required(ExpertoCrear), name='experto_crear'),
# url(r'^experto_editar/(?P<id_experto>\d+)/$', login_required(ExpertoEditar), name='experto_editar'),
# url(r'^experto_eliminar/(?P<id_experto>\d+)/$', login_required(ExpertoEliminar), name='experto_eliminar'),
# url(r'^docente_listar$', login_required(DocenteListar), name='docente_listar'),
# url(r'^docente_crear$', DocenteCrear, name='docente_crear'),
# url(r'^docente_editar/(?P<id_docente>\d+)/$', login_required(DocenteEditar), name='docente_editar'),
# url(r'^docente_eliminar/(?P<id_docente>\d+)/$', login_required(DocenteEliminar), name='docente_eliminar'),
# url(r'^representante_listar$', RepresentanteListar, name='representante_listar'),
# url(r'^representante_crear$', representanteCrear, name='representante_crear'),
# url(r'^representante_editar/(?P<id_representante>\d+)/$', login_required(RepresentanteEditar),
#     name='representante_editar'),
# url(r'^representante_eliminar/(?P<id_representante>\d+)/$', login_required(RepresentanteEliminar),
#     name='representante_eliminar'),
