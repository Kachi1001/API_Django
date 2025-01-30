from django.urls import path
from . import api
from Home.api import Log_list
urlpatterns = [
    path('app', api.app),
    path('log', Log_list.as_view()),
]