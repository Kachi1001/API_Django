from django.urls import path
from . import api

urlpatterns = [
    path('tabela/<str:table>', api.tabela),
    path('register', api.register),
    path('get_data', api.get_data),
    path('delete', api.deletar),
    path('update', api.update),
    path('select', api.select),
    path('get_list', api.get_list),
    path('function', api.funcao),
]