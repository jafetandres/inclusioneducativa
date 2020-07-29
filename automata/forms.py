from django import forms

from automata.models import TestLenguaje


class TestLenguajeForm(forms.ModelForm):
    class Meta:
        model = TestLenguaje
        fields = "__all__"
