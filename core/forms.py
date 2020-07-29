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
    class Meta:
        model = Docente
        fields = "__all__"


class ExpertoForm(forms.ModelForm):
    class Meta:
        model = Experto
        fields = "__all__"


class RepresentanteForm(forms.ModelForm):
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
