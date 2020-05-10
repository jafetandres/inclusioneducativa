from django.db import models

# Create your models here.
from InclusionEducativa.Apps.AppDocente.models import *
from InclusionEducativa.Apps.AppRepresentante.models import *

from InclusionEducativa.Apps.GestionSistema.models import Usuario


class Comentario(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, null=True, blank=True)
    contenido = models.CharField(max_length=500, null=True, blank=True)
    fechaCreacion = models.DateTimeField(auto_now=True, null=True, blank=True)
    usernameEmisor = models.CharField(max_length=500, null=True, blank=True)

class ExpertoFichaInformativa(models.Model):
    fichaInformativaDocente = models.ForeignKey(FichaInformativaDocente, on_delete=models.CASCADE, null=True,
                                                blank=True)
    fichaInformativaRepresentante = models.ForeignKey(FichaInformativaRepresentante, on_delete=models.CASCADE,
                                                      null=True, blank=True)
    experto = models.ForeignKey(Experto, on_delete=models.CASCADE, null=True, blank=True)
