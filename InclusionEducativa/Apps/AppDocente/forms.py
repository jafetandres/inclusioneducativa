from django import forms

from InclusionEducativa.Apps.AppDocente.models import *


class FichaInformativaForm(forms.ModelForm):
    class Meta:
        model = FichaInformativa
        fields = "__all__"


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = "__all__"


class fichaEstudianteForm(forms.ModelForm):
    class Meta:
        model = EstudianteDocente
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
