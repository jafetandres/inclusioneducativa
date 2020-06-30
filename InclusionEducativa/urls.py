import notifications.urls
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from InclusionEducativa.Apps.GestionSistema.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('InclusionEducativa.Apps.chat.urls', namespace='chat')),
    path('automata/', include('InclusionEducativa.Apps.automata.urls', namespace='automata')),
    path('', index, name='index'),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('appexperto/', include('InclusionEducativa.Apps.AppExperto.urls', namespace='appexperto')),
    path('gestionsistema/', include('InclusionEducativa.Apps.GestionSistema.urls', namespace='gestionsistema')),
    path('appdocente/', include('InclusionEducativa.Apps.AppDocente.urls', namespace='appdocente')),
    path('apprepresentante/', include('InclusionEducativa.Apps.AppRepresentante.urls', namespace='apprepresentante')),
    path('Chat/', include('django_chatter.urls')),
    url('^', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
