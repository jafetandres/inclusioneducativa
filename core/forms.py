import datetime
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from core.models import *


class UsuarioForm(forms.ModelForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = Usuario.objects.exclude(pk=self.instance.pk).get(username=username)
        except Usuario.DoesNotExist:
            return username
        raise forms.ValidationError(u'"%s" ya esta en uso.' % username)

    def clean_fechaNacimiento(self):
        fechaNacimiento = self.cleaned_data['fechaNacimiento']
        if fechaNacimiento > datetime.date.today():
            raise forms.ValidationError("La fecha de nacimiento es incorrecta")
        return fechaNacimiento

    class Meta:
        model = Usuario
        fields = "__all__"


class DocenteForm(forms.ModelForm):
    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        valores = [int(cedula[x]) * (2 - x % 2) for x in range(9)]
        suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
        if int(cedula[9]) == 10 - int(str(suma)[-1:]):
            return cedula
        else:
            raise forms.ValidationError("Cédula incorrecta")

    class Meta:
        model = Docente
        fields = "__all__"


class ExpertoForm(forms.ModelForm):
    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        valores = [int(cedula[x]) * (2 - x % 2) for x in range(9)]
        suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
        if int(cedula[9]) == 10 - int(str(suma)[-1:]):
            return cedula
        else:
            raise forms.ValidationError("Cédula incorrecta")

    class Meta:
        model = Experto
        fields = "__all__"


class RepresentanteForm(forms.ModelForm):
    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        valores = [int(cedula[x]) * (2 - x % 2) for x in range(9)]
        suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
        if int(cedula[9]) == 10 - int(str(suma)[-1:]):
            return cedula
        else:
            raise forms.ValidationError("Cédula incorrecta")

    class Meta:
        model = Representante
        fields = "__all__"


class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion

        fields = "__all__"


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = "__all__"


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
