from django.template import Library

register = Library()

@register.filter(name="es_institucion_selecionada")
def es_institucion_selecionada(instituciones, institucion):

    for insti in instituciones:
        if insti.id == institucion.id:
            return True
    return False
