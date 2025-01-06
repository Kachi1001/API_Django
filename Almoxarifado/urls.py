from django.urls import path
from .api import *
urlpatterns = [
  path('epi_movimentacao', epimovimentacao_list.as_view()),
  path('epi_movimentacao/<int:pk>', epimovimentacao_detail.as_view()),
  path('epi_cadastro', epicadastro_list.as_view()),
  path('epi_cadastro/<int:pk>', epicadastro_detail.as_view()),
  path('produto', produto_list.as_view()),
  path('produto/<int:pk>', produto_detail.as_view()),
  
  
  path('tabela/<str:table>', tabela),
  path('resource/<str:name>', resource),
  path('select/<str:resource>', select),
  path('grafico/<str:resource>', grafico),  
]