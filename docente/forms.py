from django import forms
from docente.models import *


class FichaInformativaDocenteForm(forms.ModelForm):
    def selected_genders_labels(self):
        return [label for value, label in self.fields['dificultadesAula'].choices if
                value in self['dificultadesAula'].value()]

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
