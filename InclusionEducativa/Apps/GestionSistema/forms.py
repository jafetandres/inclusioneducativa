import datetime

from django import forms
from InclusionEducativa.Apps.GestionSistema.models import Experto, Docente, Representante, Institucion, Usuario


class UsuarioForm(forms.ModelForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = Usuario.objects.exclude(pk=self.instance.pk).get(username=username)
        except Usuario.DoesNotExist:
            return username
        raise forms.ValidationError(u'El Correo "%s" ya esta en uso.' % username)

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


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
