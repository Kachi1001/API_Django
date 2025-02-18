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

  path('ferias_processadas', FeriasProcessadas_list.as_view()),
  path('ferias_processadas/<str:pk>', FeriasProcessadas_detail.as_view()),

  path('periodo_aquisitivo', PeriodoAquisitivo_list.as_view()),
  path('periodo_aquisitivo_funcao', PeriodoAquisitivo_funcao),
  path('periodo_aquisitivo/<str:pk>', PeriodoAquisitivo_detail.as_view()),
  
  path('ferias_utilizadas', FeriasUtilizadas_list.as_view()),
  path('ferias_utilizadas/<str:pk>', FeriasUtilizadas_detail.as_view()),

  path('tipoavaliacao', TipoAvaliacao_list.as_view()),
  path('tipoavaliacao/<str:pk>', TipoAvaliacao_detail.as_view()),

  path('feriado', Feriado_list.as_view()),
  path('feriado/<str:pk>', Feriado_detail.as_view()),

  path('integracao', Integracao_list.as_view()),
  path('integracao/<str:pk>', Integracao_detail.as_view()),
  path('integracao_nr', IntegracaoNr_list.as_view()),
  path('integracao_nr/<str:pk>', IntegracaoNr_detail.as_view()),
  path('integracao_nr_tipo', IntegracaoNrTipo_list.as_view()),
  path('integracao_nr_tipo/<str:pk>', IntegracaoNrTipo_detail.as_view()),
  path('integracao_epi', IntegracaoEpi_list.as_view()),
  path('integracao_epi/<str:pk>', IntegracaoEpi_detail.as_view()),
  
  path('insalubridade', Insalubridade_list.as_view()),
  path('insalubridade/<str:pk>', Insalubridade_detail.as_view()),

  # path('horas_ponto', HorasPonto_list.as_view()),
  path('horas_ponto_import', HorasPonto_import),
  # path('horas_ponto/<str:pk>', HorasPonto_detail.as_view()),
  
  path('tabela', tabela_list),
  path('tabela/<str:table>', tabela),
  path('resource/<str:name>', resource),
  path('select/<str:resource>', select),
  path('grafico/<str:resource>', grafico),
  

  path('ponto', Lembrete_list.as_view()),
  path('ponto/<str:pk>', Lembrete_detail.as_view()),

  path('lembrete', Lembrete.as_view()),
  
  path('app/feriado', app_feriado),
  path('app/<str:app>', app_menu),
]