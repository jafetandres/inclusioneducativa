from InclusionEducativa.Apps.AppDocente.models import *
from InclusionEducativa.Apps.AppRepresentante.models import *
from InclusionEducativa.Apps.GestionSistema.models import Usuario


class ExpertoFichaInformativa(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, null=True, blank=True)
    fichaInformativaDocente = models.ForeignKey(FichaInformativaDocente, on_delete=models.CASCADE, null=True,
                                                blank=True)
    fichaInformativaRepresentante = models.ForeignKey(FichaInformativaRepresentante, on_delete=models.CASCADE,
                                                      null=True, blank=True)
    experto = models.ForeignKey(Experto, on_delete=models.CASCADE, null=True, blank=True)
