from django import forms

from InclusionEducativa.Apps.AppRepresentante.models import *


class FichaEstudianteForm(forms.ModelForm):
    class Meta:
        model = EstudianteRepresentante
        fields = "__all__"


class DificultadForm(forms.ModelForm):
    class Meta:
        model = Dificultad
        fields = "__all__"


class DiagnosticoMedicoForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoMedico
        fields = "__all__"
