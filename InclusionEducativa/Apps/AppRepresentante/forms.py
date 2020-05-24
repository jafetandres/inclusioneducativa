from django import forms

from InclusionEducativa.Apps.AppRepresentante.models import *


class FichaInformativaRepresentanteForm(forms.ModelForm):
    class Meta:
        model = FichaInformativaRepresentante
        fields = "__all__"

class DificultadForm(forms.ModelForm):
    class Meta:
        model = Dificultad
        fields = "__all__"


class DiagnosticoMedicoForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoMedico
        fields = "__all__"
