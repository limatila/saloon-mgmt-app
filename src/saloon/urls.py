from .views import renderers
from django.urls import path

urlpatterns = [
    path('', renderers.redirectHome, name='root'),
    path('home', renderers.home, name='home'),
    path('base', renderers.base, name='base-debug')
]