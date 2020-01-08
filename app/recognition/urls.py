from django.urls import path
from . import views

app_name = 'recognition'

urlpatterns = [
    path('activate', views.activate_device, name='activate'),
]
