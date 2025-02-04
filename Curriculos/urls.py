from django.urls import path
from .api import *

urlpatterns = [
  path('candidato', candidato_list.as_view()),
  path('candidato/<int:pk>', candidato_detail.as_view()),

  path('escolaridade', escolaridade_list.as_view()),
  path('escolaridade/<int:pk>', escolaridade_detail.as_view()),
  
  path('experiencia', experiencia_list.as_view()),
  path('experiencia/<int:pk>', experiencia_detail.as_view()),
  
  path('questionario', questionario_list.as_view()),
  path('questionario/<int:pk>', questionario_detail.as_view()),
  
  path('percepcao', percepcao_list.as_view()),
  path('percepcao/<int:pk>', percepcao_detail.as_view()),
  
  path('entrevista', entrevista_list.as_view()),
  path('entrevista/<int:pk>', entrevista_detail.as_view()),
  
  path('profissoes', Profissoes_list.as_view()),
  path('profissoes/<int:pk>', Profissoes_detail.as_view()),
  
  path('anexos', Anexos_list.as_view()),
  path('anexos/<str:pk>', Anexos_detail.as_view()),
 
  path('setor', Setor_list.as_view()),
  path('setor/<str:pk>', Setor_detail.as_view()),
 
  path('area_atuacao', AreaAtuacao_list.as_view()),
  path('area_atuacao/<str:pk>', AreaAtuacao_detail.as_view()),
 
  path('classificacao', Classificacao_list.as_view()),
  path('classificacao/<str:pk>', Classificacao_detail.as_view()),
 
  path('tabela', tabela_list),
  path('tabela/<str:table>', tabela),
  path('resource/<str:name>', resource),
  path('select/<str:resource>', select),
  path('grafico/<str:resource>', grafico),  
]