from django.urls import path
from . import api

urlpatterns = [
    # path('register', api.register),
    # path('get_table', api.get_table),
    # path('get_data', api.get_data),
    # path('deletar', api.deletar),
    # path('update', api.update),
    path('colaborador', api.Colaborador_list.as_view()),
    path('colaborador/<str:pk>', api.Colaborador_detail.as_view()),
    
    path('obra', api.Obra_list.as_view()),
    path('obra/<str:pk>', api.Obra_detail.as_view()),
    
    path('funcao', api.Funcao_list.as_view()),
    path('funcao/<str:pk>', api.Funcao_detail.as_view()),
    
    path('supervisor', api.Supervisor_list.as_view()),
    path('supervisor/<str:pk>', api.Supervisor_detail.as_view()),
    
    path('atividade', api.Atividade_list.as_view()),
    path('atividade/<str:pk>', api.Atividade_detail.as_view()),

    path('diario', api.Diarioobra_list.as_view()),
    path('diario/<str:pk>', api.Diarioobra_detail.as_view()),
    path('diario_impressao', api.diario_impressao),
    
    path('programacao', api.Programacao_list.as_view()),
    path('programacao/<str:pk>', api.Programacao_detail.as_view()),
    
    path('select/<str:resource>', api.select),
    path('resource/<str:name>', api.resource),
    
    path('exec/<str:funcao>', api.funcao),
    path('tabela/<str:table>', api.tabela),
    path('grafico/<str:table>', api.grafico),
]