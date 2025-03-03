from django.urls import path

from .api import *
urlpatterns = [
  path('epi_movimentacao', epimovimentacao_list.as_view()),
  path('epi_movimentacao/<int:pk>', epimovimentacao_detail.as_view()),
  path('epi_cadastro', epicadastro_list.as_view()),
  path('epi_cadastro/<int:pk>', epicadastro_detail.as_view()),
  path('produto', produto_list.as_view()),
  path('produto/<int:pk>', produto_detail.as_view()),
  path('numeracao', Numeracao_list.as_view()),
  path('numeracao/<int:pk>', Numeracao_detail.as_view()),
  
  path('ficha', Ficha_list.as_view()),
  path('ficha/<str:pk>', Ficha_detail.as_view()),
  path('ficha_impressao', get_impressao),
  
  path('ficha_padrao', FichaPadrao_list.as_view()),
  path('ficha_padrao/<str:pk>', FichaPadrao_detail.as_view()),

  path('erros', Erros_list.as_view()),
  path('erros/<str:pk>', Erros_detail.as_view()),
  
  path('digitalizacao', Digitalizacao_list.as_view()),
  path('digitalizacao/<str:pk>', Digitalizacao_detail.as_view()),
  
  
  path('epis_validos', EpisValidos.as_view()),
  path('colaborador/<int:pk>', colaborador.as_view()),
  
  
  path('verifica_ca/<int:ca>', verificarCA),
  
  path('funcao/<str:method>', funcao),
  path('tabela/<str:table>', tabela),
  path('resource/<str:name>', resource),
  path('select/<str:resource>', select),
  path('grafico/<str:resource>', grafico),  
]