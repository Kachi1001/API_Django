import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from . import models, views, serializers
from Site_django import util
    
# Configurações de conexão com o banco de dados PostgreSQL


resources = util.get_resources(models)
table_models = util.get_classes(models)
table_views = util.get_classes(views)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tabela(request, table):
    dicts = table_models
    dicts.update(table_views)
    return util.get_table(request, table, dicts)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def grafico(request, resource):
    from . import views
    graficos = {
        'horas': views.Graficos,
    }
    from django.core.exceptions import ObjectDoesNotExist
    try:
        dados = graficos.get(resource).objects.all().values()
        dados = dados[len(dados) -36:]
        return Response(dados,status=200)
    except ObjectDoesNotExist:
        return Response({'method':'Alerta de pesquisa','message': f'id não encontrada <{id}>' }, status=404)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def select(request, resource):
    from .serializers import Select

    return util.create_select(request, resource, Select)


@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def resource(request, name):
    return Response(resources.get(name))


class ExtratoBancario_list(util.LC):
    serializer_class = serializers.Extrato_bancario
    queryset = serializer_class.Meta.model.objects.all()
    
    @util.database_exception
    def create(self, request, *args, **kwargs):
        for x in request.POST:
            linha = self.serializers_class(data=x)
            if linha.is_valid():
                linha.save
            else:
                return Response(linha.errors,status=406)
        return Response({'Sucesso'},status=201)
    
