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


class EstudianteDocente(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True, blank=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(unique=True, max_length=50, null=True, blank=True)
    fechaNacimiento = models.DateField()
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True, blank=True)
    nivelCursa = models.CharField(max_length=50)
    dificultad = models.ForeignKey(Dificultad, on_delete=models.CASCADE, null=True, blank=True)
    tipoFamilia = models.CharField(max_length=50, null=True, blank=True)
    dinamicaFamiliar = models.CharField(max_length=50, null=True, blank=True)
    antecedentesFPatologicos = models.CharField(max_length=50, null=True, blank=True)
    diagnosticoMedico = models.ForeignKey(DiagnosticoMedico, on_delete=models.CASCADE, null=True, blank=True)
    diagnosticoSindromico = models.ForeignKey(DiagnosticoSindromico, on_delete=models.CASCADE, null=True, blank=True)
    emisionDiagnosticoSindromico = models.CharField(max_length=50, null=True, blank=True)
    detalleDificultades = models.CharField(max_length=1024, null=True, blank=True)


class ExpertoFicha(models.Model):
    ficha = models.ForeignKey(EstudianteDocente, on_delete=models.CASCADE, null=True, blank=True)
    experto = models.ForeignKey(Experto, on_delete=models.CASCADE, null=True, blank=True)


class EstudianteTest(models.Model):
    resultado = models.CharField(max_length=50, null=True, blank=True)
    # p1r2 = models.CharField(max_length=50, null=True, blank=True)
    # p1r3 = models.CharField(max_length=50, null=True, blank=True)
    # p1r4 = models.CharField(max_length=50, null=True, blank=True)
    # p1r5 =models.CharField(max_length=50, null=True, blank=True)
    # r6 = models.CharField(max_length=50, null=True, blank=True)
    # r7 = models.CharField(max_length=50, null=True, blank=True)
    # r8 = models.CharField(max_length=50, null=True, blank=True)
    # r9 = models.CharField(max_length=50, null=True, blank=True)
    # r10 = models.CharField(max_length=50, null=True, blank=True)
    # r11 = models.CharField(max_length=50, null=True, blank=True)
    # r12 = models.CharField(max_length=50, null=True, blank=True)
    # r13 = models.CharField(max_length=50, null=True, blank=True)
    # r14 = models.CharField(max_length=50, null=True, blank=True)
    # r15 = models.CharField(max_length=50, null=True, blank=True)
    # r16 = models.CharField(max_length=50, null=True, blank=True)
