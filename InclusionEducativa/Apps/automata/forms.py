from django import forms

from InclusionEducativa.Apps.automata.models import TestLenguaje


class TestLenguajeForm(forms.ModelForm):
    class Meta:
        model = TestLenguaje
        fields = "__all__"
