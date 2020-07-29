import notifications.urls
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from core.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls', namespace='chat')),
    path('automata/', include('automata.urls', namespace='automata')),
    path('', index, name='index'),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('appexperto/', include('experto.urls', namespace='appexperto')),
    path('gestionsistema/', include('core.urls', namespace='gestionsistema')),
    path('appdocente/', include('docente.urls', namespace='appdocente')),
    path('apprepresentante/', include('representante.urls', namespace='apprepresentante')),
    path('page/', include('pages.urls')),
    # path('Chat/', include('django_chatter.urls')),
    url('^', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
