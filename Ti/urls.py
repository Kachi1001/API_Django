from django.urls import path
from . import api

urlpatterns = [
    path('app', api.app),
]