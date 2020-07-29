from django.urls import path
from automata.views import *

app_name = 'automata'
urlpatterns = [
    path('datosTest/', datosTest, name='datosTest'),
    path('test/', test, name='test'),
    path('resultadoTest/', resultadoTest, name='resultadoTest'),
]