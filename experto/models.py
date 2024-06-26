from docente.models import *
from representante.models import *
from django.dispatch import receiver
from django.db.models.signals import post_save

class ExpertoFichaInformativa(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, null=True, blank=True)
    fichaInformativaDocente = models.ForeignKey(FichaInformativaDocente, on_delete=models.CASCADE, null=True,
                                                blank=True)
    fichaInformativaRepresentante = models.ForeignKey(FichaInformativaRepresentante, on_delete=models.CASCADE,
                                                      null=True, blank=True)
    experto = models.ForeignKey(Experto, on_delete=models.CASCADE, null=True, blank=True)



