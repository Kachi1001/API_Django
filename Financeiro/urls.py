from django.urls import path
from . import api

urlpatterns = [
    # path('register', api.register),
    # path('get_table', api.get_table),
    # path('get_data', api.get_data),
    # path('deletar', api.deletar),
    # path('update', api.update),
    path('extrato_bancario', api.ExtratoBancario_list.as_view()),
    path('caixa_import', api.caixa_import),
    # path('obra', api.Obra_list.as_view()),
    # path('obra/<str:pk>', api.Obra_detail.as_view()),

]