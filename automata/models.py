from django.db import models

from core.models import Usuario


class Canton(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)


class TestLenguaje(models.Model):
    canton = models.ForeignKey(Canton, on_delete=models.CASCADE, null=True, blank=True)
    fechaNacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=100, null=True, blank=True)
    discapacidad = models.CharField(max_length=100, null=True, blank=True)
    p1 = models.CharField(max_length=5, null=True, blank=True)
    p2 = models.CharField(max_length=5, null=True, blank=True)
    p3 = models.CharField(max_length=5, null=True, blank=True)
    p4 = models.CharField(max_length=5, null=True, blank=True)
    p5 = models.CharField(max_length=5, null=True, blank=True)
    p6 = models.CharField(max_length=5, null=True, blank=True)
    p7 = models.CharField(max_length=5, null=True, blank=True)
    p8 = models.CharField(max_length=5, null=True, blank=True)
    p9 = models.CharField(max_length=5, null=True, blank=True)
    p10 = models.CharField(max_length=5, null=True, blank=True)
    p11 = models.CharField(max_length=5, null=True, blank=True)
    p12 = models.CharField(max_length=5, null=True, blank=True)
    p13 = models.CharField(max_length=5, null=True, blank=True)
    p14 = models.CharField(max_length=5, null=True, blank=True)
    p15 = models.CharField(max_length=5, null=True, blank=True)
    p16 = models.CharField(max_length=5, null=True, blank=True)
    p17 = models.CharField(max_length=5, null=True, blank=True)
    p18 = models.CharField(max_length=5, null=True, blank=True)
    p19 = models.CharField(max_length=5, null=True, blank=True)
    p20 = models.CharField(max_length=5, null=True, blank=True)
    p21 = models.CharField(max_length=5, null=True, blank=True)
    p22 = models.CharField(max_length=5, null=True, blank=True)
    p23 = models.CharField(max_length=5, null=True, blank=True)
    p24 = models.CharField(max_length=5, null=True, blank=True)
    p25 = models.CharField(max_length=5, null=True, blank=True)
    p26 = models.CharField(max_length=5, null=True, blank=True)
    p27 = models.CharField(max_length=5, null=True, blank=True)
    p28 = models.CharField(max_length=5, null=True, blank=True)
    p29 = models.CharField(max_length=5, null=True, blank=True)
    p30 = models.CharField(max_length=5, null=True, blank=True)
    p31 = models.CharField(max_length=5, null=True, blank=True)
    p32 = models.CharField(max_length=5, null=True, blank=True)
    p33 = models.CharField(max_length=5, null=True, blank=True)
    p34 = models.CharField(max_length=5, null=True, blank=True)
    p35 = models.CharField(max_length=5, null=True, blank=True)
    p36 = models.CharField(max_length=5, null=True, blank=True)
    p37 = models.CharField(max_length=5, null=True, blank=True)
    p38 = models.CharField(max_length=5, null=True, blank=True)


class ResumenExperto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    audio = models.FileField(upload_to='audio/')
