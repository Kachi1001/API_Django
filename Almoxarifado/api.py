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
serializer_dicts = util.generate_serializer_dicts(serializers)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tabela(request, table):
    dicts = table_models
    dicts.update(table_views)
    return util.get_table(request, table, dicts, serializer_dicts['Table'])

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def select(request, resource):
    return util.create_select(request, resource,  serializer_dicts['Select'])

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
    
from decouple import config
from Site_django import settings
import os
from openpyxl import load_workbook

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_impressao(request):
    input_data = request.GET
    if 'ficha' not in input_data:
        return Response({'message': 'Parâmetro "ficha" não informado'}, status=400)

    # Sanitiza o nome do arquivo para evitar injeção de caminhos
    ficha = os.path.basename(input_data['ficha'])  # Remove paths
    # Define caminhos usando os.path.join para compatibilidade entre sistemas
    template_dir = os.path.join(settings.BASE_DIR, 'template', 'xlsx')
    original = os.path.join(template_dir, 'ficha_epi.xlsx')
    copia = os.path.join(template_dir, f'{ficha}.xlsx')

    output_pdf = os.path.join(config('MEDIA_ROOT'), 'Almoxarifado', 'ficha_epi', f'{ficha}.pdf')

    try:
        cab = views.CabecalhoFicha.objects.get(ficha=ficha)
        
        arquivo = load_workbook(original)
        aba = arquivo.active
        aba['J1'] = cab.nome[:1]
        aba['C5'] = cab.nome
        aba['C6'] = cab.funcao
        aba['C7'] = f'RG:  {cab.rg}'
        aba['F7'] = f'CTPS:  {cab.ctps}'
        aba['A7'] = f'FICHA:  {cab.ficha}'

        try:
            movs = models.EpiMovimentacao.objects.filter(ficha=ficha)
            tick = 14
            if len(movs) > 29:
                return Response({'message': 'Número de movimentações excede o limite de 29'}, status=400)
            for mov in movs:
                aba[f'A{tick}'] = mov.quantidade
                aba[f'B{tick}'] = mov.produto.produto
                aba[f'D{tick}'] = mov.tamanho
                aba[f'E{tick}'] = mov.data_entrega.strftime('%d/%m/%Y')
                aba[f'G{tick}'] = mov.epi_cadastro.fabricante
                aba[f'H{tick}'] = mov.epi_cadastro.ca
                aba[f'I{tick}'] = mov.epi_cadastro.validade.strftime('%d/%m/%Y')
                tick += 1
        except models.EpiMovimentacao.DoesNotExist:
            pass

        
        arquivo.save(copia)
        util.excel_to_pdf_libreoffice(copia, output_pdf)
        os.remove(copia)
        return Response({'message': 'Arquivo processado', 'pdf_path': f'http://tecnikaengenharia.ddns.net/media/Almoxarifado/ficha_epi/{input_data['ficha']}.pdf'})

    except FileNotFoundError as e:
        return Response({'message': f'Arquivo template não encontrado {str(e)}'}, status=500)
    except PermissionError:
        return Response({'message': f'Permissão negada para escrever no diretório {str(e)}'}, status=500)
    except Exception as e:
        return Response({'message': f'Erro interno: {str(e)}'}, status=500)