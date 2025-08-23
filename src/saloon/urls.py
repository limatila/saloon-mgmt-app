from django.conf.urls.static import static as staticLoader
from django.urls import path
from django.conf import settings
from .views import renderers

urlpatterns = [
    #main
    path('', renderers.REDIRECT_HOME, name='root'),
    path('admin-redirection', renderers.REDIRECT_ADMIN, name="admin-redirection"),
    path('base', renderers.BASE, name='base-debug'),
    path('home', renderers.HOME, name='home'),

    #per view
    path('workers', renderers.DYNAMIC_RENDER, name='workers'),
    path('appointments', renderers.DYNAMIC_RENDER, name='appointments'),
    path('clients', renderers.DYNAMIC_RENDER, name='clients'),

    #forms
    path('new-appointment', renderers.REGISTRATION_APPOINTMENTS, name="schedule-appointment"),
    path('new-worker', renderers.REGISTRATION_WORKERS, name="register-worker")
]

#! statics, remove for production
urlpatterns.extend(
    #So the server can see into the static files, in DEBUG mode.
    staticLoader(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
urlpatterns.extend(
    staticLoader(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)