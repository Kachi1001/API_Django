from django.urls import path
from . import api

urlpatterns = [
    path('funcao', api.funcao),
    path('tabela/<str:table>', api.tabela),
    path('register', api.register),
    path('get_table', api.get_table),
    path('get_data', api.get_data),
    path('deletar', api.deletar),
    path('update', api.update),
    path('grafico', api.grafico),
    path('diario', api.diario),
]