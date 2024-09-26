from django.urls import path
from . import api

urlpatterns = [
    path('register', api.register),
    path('get', api.get),
    path('delete', api.delete),
    path('edit', api.edit),
    path('reservasala', api.reservaSala),
]