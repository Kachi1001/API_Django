from django.urls import path
from .api import *
odio = {'get':'get', 'post':'post'}
urlpatterns = [
    path('colaborador', colaborador_list.as_view()),
    path('colaborador/<int:pk>', colaborador_detail.as_view()),
    
    path('funcao', funcao_list.as_view()),
    path('funcao/<str:pk>', funcao_detail.as_view()),
    
    path('ocupacao', ocupacao_list.as_view()),
    path('ocupacao_alterar/<str:pk>', ocupacao_alterar),
    path('ocupacao_disidio/<str:pk>', ocupacao_disidio),
    path('ocupacao/<str:pk>', ocupacao_detail.as_view()),
    
    path('feriasprocessadas', FeriasProcessadas_list.as_view(odio)),
    path('feriasprocessadas/<str:pk>', FeriasProcessadas_detail.as_view()),
    
    path('feriasutilizadas', FeriasUtilizadas_list.as_view(odio)),
    path('feriasutilizadas/<str:pk>', FeriasUtilizadas_detail.as_view()),
    
    path('tabela/<str:table>', tabela),
    
    
    # path('register', api.register),
    # path('get_data', api.get_data),
    # path('delete', api.deletar),
    # path('update', api.update),
    # path('select', api.select),
    # path('get_list', api.get_list),
    # path('function', api.funcao),
    # path('lembrete/<str:acao>', api.lembrete)
]