from .views import renderers
from django.urls import path

urlpatterns = [
    path('', renderers.REDIRECT_HOME, name='root'),
    path('base', renderers.BASE, name='base-debug'),
    path('home', renderers.HOME, name='home'),
    path('workers', renderers.WORKERS, name='workers'),
    path('appointments', renderers.APPOINTMENTS, name='appointments')
]