from django.db import models
from core.models import *


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


class FichaInformativaRepresentante(models.Model):
    representante = models.ForeignKey(Representante, on_delete=models.CASCADE, null=True, blank=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, null=True, blank=True)
    dificultad = models.ForeignKey(Dificultad, on_delete=models.CASCADE, null=True, blank=True)
    tipoFamilia = models.CharField(max_length=50, null=True, blank=True)
    tipoFamiliaDescripcion = models.CharField(max_length=500, null=True, blank=True)
    dinamicaFamiliar = models.CharField(max_length=50, null=True, blank=True)
    antecedentesFPatologicos = models.CharField(max_length=50, null=True, blank=True)
    antecedentesFPatologicosDescripcion = models.CharField(max_length=500, null=True, blank=True)
    diagnosticoMedico = models.ForeignKey(DiagnosticoMedico, on_delete=models.CASCADE, null=True, blank=True)
    detalleDificultades = models.CharField(max_length=1024, null=True, blank=True)
