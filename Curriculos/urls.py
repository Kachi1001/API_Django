from django.urls import path
from .api import *

urlpatterns = [
  path('candidato', candidato_list.as_view()),
  path('candidato/<int:pk>', candidato_detail.as_view()),

  path('tabela/<str:table>', tabela),
  path('resource/<str:name>', resource),
  path('select/<str:resource>', select),
  path('grafico/<str:resource>', grafico),  
]