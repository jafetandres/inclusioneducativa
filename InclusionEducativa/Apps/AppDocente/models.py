from django.db import models
from InclusionEducativa.Apps.GestionSistema.models import *


class Dificultad(models.Model):
    respuesta_prenatal = models.CharField(max_length=50)
    descripcion_prenatal = models.CharField(max_length=50, null=True, blank=True)
    respuesta_perinatal = models.CharField(max_length=50)
    descripcion_perinatal = models.CharField(max_length=50, null=True, blank=True)
    respuesta_postnatal = models.CharField(max_length=50)
    descripcion_postnatal = models.CharField(max_length=50, null=True, blank=True)


class DiagnosticoMedico(models.Model):
    diagnosticoMedicoRespuesta = models.CharField(max_length=50, null=True, blank=True)
    diagnosticoMedicoOpcion = models.CharField(max_length=50, null=True, blank=True)
    diagnosticoMedicoDescripcion = models.CharField(max_length=500, null=True, blank=True)


class DiagnosticoSindromico(models.Model):
    diagnosticoSindromicoRespuesta = models.CharField(max_length=50, null=True, blank=True)
    diagnosticoSindromicoOpcion = models.CharField(max_length=50, null=True, blank=True)
    diagnosticoSindromicoDescripcion = models.CharField(max_length=500, null=True, blank=True)


class FichaEstudiante(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, null=True, blank=True)
    dificultad = models.ForeignKey(Dificultad, on_delete=models.CASCADE, null=True, blank=True)
    tipoFamilia = models.CharField(max_length=50, null=True, blank=True)
    dinamicaFamiliar = models.CharField(max_length=50, null=True, blank=True)
    antecedentesFPatologicos = models.CharField(max_length=50, null=True, blank=True)
    diagnosticoMedico = models.ForeignKey(DiagnosticoMedico, on_delete=models.CASCADE, null=True, blank=True)
    diagnosticoSindromico = models.ForeignKey(DiagnosticoSindromico, on_delete=models.CASCADE, null=True, blank=True)
    emisionDiagnosticoSindromico = models.CharField(max_length=50, null=True, blank=True)
    detalleDificultades = models.CharField(max_length=1024, null=True, blank=True)


# class ExpertoFicha(models.Model):
#     ficha = models.ForeignKey(EstudianteDocente, on_delete=models.CASCADE, null=True, blank=True)
#     experto = models.ForeignKey(Experto, on_delete=models.CASCADE, null=True, blank=True)


class EstudianteTest(models.Model):
    resultado = models.CharField(max_length=50, null=True, blank=True)

