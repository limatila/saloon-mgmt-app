from . import views
from django.urls import path

urlpatterns = [
    path('', views.redirectHome, name='root'),
    path('home', views.home, name='home')
]