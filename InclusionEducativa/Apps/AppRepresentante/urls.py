from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from InclusionEducativa.Apps.AppRepresentante.views import *

urlpatterns = [
    url(r'^$', login_required(base), name='base'),
    url(r'^fichaEstudianteCrear$', login_required(fichaEstudianteCrear), name='fichaEstudianteCrear'),

]
