from django.urls import path
from .api import *
odio = {'get':'get', 'post':'post'}
urlpatterns = [
  path('colaborador', colaborador_list.as_view()),
  path('colaborador/<int:pk>', colaborador_detail.as_view()),
  path('colaborador_desligamento/<int:pk>', colaborador_desligamento),

  path('funcao', funcao_list.as_view()),
  path('funcao/<str:pk>', funcao_detail.as_view()),

  path('equipe', equipe_list.as_view()),
  path('equipe/<str:pk>', equipe_detail.as_view()),

  path('ocupacao', ocupacao_list.as_view()),
  path('ocupacao_alterar', ocupacao_alterar),
  path('ocupacao_dissidio', ocupacao_dissidio),
  path('ocupacao/<str:pk>', ocupacao_detail.as_view()),

  path('feriasprocessadas', FeriasProcessadas_list.as_view()),
  path('feriasprocessadas/<str:pk>', FeriasProcessadas_detail.as_view()),

  path('periodo_aquisitivo', PeriodoAquisitivo_list.as_view()),
  path('periodo_aquisitivo_funcao', PeriodoAquisitivo_funcao),
  path('periodo_aquisitivo/<str:pk>', PeriodoAquisitivo_detail.as_view()),
  
  path('feriasutilizadas', FeriasUtilizadas_list.as_view()),
  path('feriasutilizadas/<str:pk>', FeriasUtilizadas_detail.as_view()),

  path('tabela/<str:table>', tabela),

  path('select/<str:resource>', select),
  # path('lembrete', )
  # path('register', api.register),
  # path('get_data', api.get_data),
  # path('delete', api.deletar),
  # path('update', api.update),
  # path('select', api.select),
  # path('get_list', api.get_list),
  # path('function', api.funcao),
  # path('lembrete/<str:acao>', api.lembrete)
]