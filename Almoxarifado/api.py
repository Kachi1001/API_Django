from . import models, views, serializers
from rest_framework.response import Response
from Site_django import util
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

table_models = util.get_classes(models)
table_views = util.get_classes(views)
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tabela(request, table):
    dicts = table_models
    dicts.update(table_views)
    return util.get_table(request, table, dicts, serializers.Table)

resources = util.get_resources(models)
resources['epi_movimentacao']['select'] += ['colaborador','obra','produto']

@api_view(['GET'])
def resource(request, name):
    if resources.get(name):
        return Response(resources.get(name))
    else:
        return Response({'Error, não encontrado o recurso'}, status=404)

  
from . import views
graficos = {
    # 'ativos_rovatatividade': views.ativos_rotatividade,
}
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def grafico(request, resource):
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
        
# Colaborador
class epimovimentacao_list(util.LC):
    serializer_class = serializers.EpiMovimentacao
    queryset = serializer_class.Meta.model.objects.all()

class epimovimentacao_detail(util.RUD):
    serializer_class = serializers.EpiMovimentacao
    queryset = serializer_class.Meta.model.objects.all()


class epicadastro_list(util.LC):
    serializer_class = serializers.EpiCadastro
    queryset = serializer_class.Meta.model.objects.all()

class epicadastro_detail(util.RUD):
    serializer_class = serializers.EpiCadastro
    queryset = serializer_class.Meta.model.objects.all()


class produto_list(util.LC):
    serializer_class = serializers.Produto
    queryset = serializer_class.Meta.model.objects.all()

class produto_detail(util.RUD):
    serializer_class = serializers.Produto
    queryset = serializer_class.Meta.model.objects.all()
    