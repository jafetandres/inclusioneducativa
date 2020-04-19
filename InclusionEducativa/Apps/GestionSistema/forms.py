from django import forms
from InclusionEducativa.Apps.GestionSistema.models import Experto, Docente, Representante, Institucion, Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model=Usuario
        fields = "__all__"


class DocenteForm(forms.ModelForm):

    class Meta:
        model=Docente
        fields = "__all__"

class ExpertoForm(forms.ModelForm):
    class Meta:
        model=Experto
        fields="__all__"


class RepresentanteForm(forms.ModelForm):
    class Meta:
        model=Representante
        fields="__all__"


class InstitucionForm(forms.ModelForm):
    class Meta:
        model=Institucion

        fields="__all__"


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)