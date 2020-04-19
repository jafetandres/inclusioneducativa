from django.db import models

# Create your models here.
from InclusionEducativa.Apps.AppDocente.models import EstudianteDocente
from InclusionEducativa.Apps.AppRepresentante.models import EstudianteRepresentante
from InclusionEducativa.Apps.GestionSistema.models import Usuario


class Comentario(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    fichaEstudiante= models.ForeignKey(EstudianteDocente,on_delete=models.CASCADE, null=True, blank=True)
    contenido = models.CharField(max_length=500, null=True, blank=True)
    fechaCreacion=models.DateTimeField(auto_now=True, null=True, blank=True)
    usernameEmisor= models.CharField(max_length=500, null=True, blank=True)

