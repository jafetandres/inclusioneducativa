from django import forms
from InclusionEducativa.Apps.AppDocente.models import *

class FichaInformativaDocenteForm(forms.ModelForm):
    class Meta:
        model = FichaInformativaDocente
        fields = "__all__"


class DificultadForm(forms.ModelForm):
    class Meta:
        model = Dificultad
        fields = "__all__"


class DiagnosticoMedicoForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoMedico
        fields = "__all__"


class DiagnosticoSindromicoForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoSindromico
        fields = "__all__"


class EstudianteTestForm(forms.ModelForm):
    class Meta:
        model = EstudianteTest
        fields = "__all__"
