from django.urls import path
from .api import *

urlpatterns = [
  path('colaborador', colaborador_list.as_view()),
  path('colaborador/<int:pk>', colaborador_detail.as_view()),
  path('colaborador_desligamento', colaborador_desligamento),

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

  path('periodoaquisitivo', PeriodoAquisitivo_list.as_view()),
  path('periodoaquisitivo_funcao', PeriodoAquisitivo_funcao),
  path('periodoaquisitivo/<str:pk>', PeriodoAquisitivo_detail.as_view()),
  
  path('feriasutilizadas', FeriasUtilizadas_list.as_view()),
  path('feriasutilizadas/<str:pk>', FeriasUtilizadas_detail.as_view()),

  path('avaliacao', Avaliacao_list.as_view()),
  path('avaliacao/<str:pk>', Avaliacao_detail.as_view()),

  path('tipoavaliacao', TipoAvaliacao_list.as_view()),
  path('tipoavaliacao/<str:pk>', TipoAvaliacao_detail.as_view()),

  path('feriado', Feriado_list.as_view()),
  path('feriado/<str:pk>', Feriado_detail.as_view()),

  
  path('tabela/<str:table>', tabela),
  path('resource/<str:name>', resource),
  path('select/<str:resource>', select),
  path('grafico/<str:resource>', grafico),
  

  path('ponto', Lembrete_list.as_view()),
  path('ponto/<str:pk>', Lembrete_detail.as_view()),
  
  path('app/feriado', app_feriado),
  path('app/<str:app>', app_menu),
]