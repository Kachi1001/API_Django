from django.urls import path
from . import api

urlpatterns = [
    path('select', api.select),
]