from django.conf.urls.static import static as staticLoader
from django.urls import path
from django.conf import settings
from .views import renderers

urlpatterns = [
    path('', renderers.REDIRECT_HOME, name='root'),
    path('base', renderers.BASE, name='base-debug'),
    path('home', renderers.HOME, name='home'),
    path('workers', renderers.WORKERS, name='workers'),
    path('appointments', renderers.APPOINTMENTS, name='appointments')
]

#!statics, remove for production
urlpatterns.extend(
    #So the server can see into the static files, in DEBUG mode.
    staticLoader(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
urlpatterns.extend(
    staticLoader(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)