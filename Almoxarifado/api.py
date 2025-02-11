import Depto_pessoal.models
from . import models, views, serializers
from rest_framework.response import Response
from Site_django import util
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import Depto_pessoal

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def funcao(request, method):
    def sql(value): 
        from Site_django.util import format_sql
        return format_sql(request.data,value)

    try:
        funcoes = {
            'baixar_tecnicon': f'baixar_tecnicon({sql('epi')},{sql('obra')})',  #nova funcao sql
            'assinar': f'assinar({sql('colab')},{sql('data')})',  #nova funcao sql
        }
        func = funcoes.get(method)
    except:
        return util.funcao_sql(request, method +'()')

    return util.funcao_sql(request, func)

table_models = util.get_classes(models)
table_views = util.get_classes(views)

table_models['colaborador'] = Depto_pessoal.models.Colaborador
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tabela(request, table):
    dicts = table_models
    dicts.update(table_views)
    return util.get_table(request, table, dicts, serializers.Table)

resources = util.get_resources(models)
resources.update(util.get_resources(views)) 
resources['epi_movimentacao']['select'] += ['colaborador','obra','produto']
resources['ficha']['select'] += ['colaborador']
resources['numeracao']['select'] += ['colaborador']
     
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
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
class colaborador(util.RUD):
    serializer_class = serializers.Colaborador
    queryset = serializer_class.Meta.model.objects.all()
    
class epimovimentacao_list(util.LC):
    serializer_class = serializers.EpiMovimentacao
    queryset = serializer_class.Meta.model.objects.all()

class epimovimentacao_detail(util.RUD):
    serializer_class = serializers.EpiMovimentacao
    queryset = serializer_class.Meta.model.objects.all()
    
    # @util.database_exception
    # def retrieve(self, request, *args, **kwargs):
    #     self.serializer_class = serializers.EpiMovimentacao.Table
    #     return super().retrieve(request, *args, **kwargs)

class epicadastro_list(util.LC):
    serializer_class = serializers.EpiCadastro
    queryset = serializer_class.Meta.model.objects.all().order_by('-id')

class epicadastro_detail(util.RUD):
    serializer_class = serializers.EpiCadastro
    queryset = serializer_class.Meta.model.objects.all()


class produto_list(util.LC):
    serializer_class = serializers.Produto
    queryset = serializer_class.Meta.model.objects.all().order_by('-id')

class produto_detail(util.RUD):
    serializer_class = serializers.Produto
    queryset = serializer_class.Meta.model.objects.all()
    
# Numeração
class Numeracao_list(util.LC):
    serializer_class = serializers.Numeracao
    queryset = serializer_class.Meta.model.objects.all().order_by('-id')

class Numeracao_detail(util.RUD):
    serializer_class = serializers.Numeracao
    queryset = serializer_class.Meta.model.objects.all()
    
# Numeração
class Ficha_list(util.LC):
    serializer_class = serializers.Ficha
    queryset = serializer_class.Meta.model.objects.all().order_by('-pagina')
    filterset_fields = ['colaborador']
    
    
class Ficha_detail(util.RUD):
    serializer_class = serializers.Ficha
    queryset = serializer_class.Meta.model.objects.all()
    
class FichaPadrao_list(util.LC):
    serializer_class = serializers.FichaPadrao
    queryset = serializer_class.Meta.model.objects.all()
class FichaPadrao_detail(util.RUD):
    serializer_class = serializers.FichaPadrao
    queryset = serializer_class.Meta.model.objects.all()
    
class EpisValidos(util.LC):
    serializer_class = serializers.EpisValidos.Table
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['id_colaborador']
    
class Erros_list(util.LC):
    serializer_class = serializers.Erros
    queryset = serializer_class.Meta.model.objects.all()
class Erros_detail(util.RUD):
    serializer_class = serializers.Erros
    queryset = serializer_class.Meta.model.objects.all()
    
from .template import template
from django.http import FileResponse
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_impressao(request):
    print(request.GET)
    
    template.excel_to_pdf_libreoffice("ficha_epi.xlsx", "temp.pdf")
    return FileResponse(open("template/temp.pdf", 'rb'), as_attachment=True)