from django.urls import path
from . import api

urlpatterns = [
  path('status', api.status, name='status'),
]