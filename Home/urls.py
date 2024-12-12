from django.urls import path
from . import api
urlpatterns = [
  path('pendencia/<str:pk>', api.pendencia_detail.as_view()),
]