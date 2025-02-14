import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import psycopg2
from django.conf import settings
from .models import *
from .views import *
import json
from .serializers import *
from Site_django import media, util
    
# Configurações de conexão com o banco de dados PostgreSQL
dbname = 'Lancamento_obra'
user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
host = settings.DATABASES['default']['HOST']
port = settings.DATABASES['default']['PORT']


def funçãoSQL(funcao): 
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    try:
        # Executando a função
        cursor.execute(f"SELECT {funcao}")
        conn.commit()
        # Retornando uma resposta de sucesso
    except psycopg2.Error as e:
        e = str(e).split('\n')[0]
        return Response({'error': e}, status=400)
    else:
        return Response({'method':'Atualizar','message':'Tabela atualizada com sucesso'}, status=200)

    finally:
        cursor.close()
        conn.close()
        

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def funcao(request, funcao):
    def get_formatter(value, padrao= None):
        value = parametro.get(value, padrao)
        if value != None:
            return "'" + str(value) + "'"
        return 'null'
        
    parametro = request.data
    if funcao == 'efetividade':
        return funçãoSQL(f"get_efetividade({get_formatter('colaborador')},{get_formatter('obra')},{get_formatter("dataini")},{get_formatter("datafim")})")
    elif funcao == 'subconsulta_lancamento':
        return funçãoSQL(f"{funcao}('{parametro.get("colaborador", '')}','{parametro.get("dia", '2050-01-01')}')")
    else:
        return funçãoSQL(funcao+'()')
        

from . import models, views, graficos, serializers
table_models = util.get_classes(models)
table_views = util.get_classes(views)
serializer_dicts = util.generate_serializer_dicts(serializers)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tabela(request, table):
    dicts = table_models
    dicts.update(table_views)
    return util.get_table(request, table, dicts, serializer_dicts['Table'])

serializer_dicts['Select']['encarregado'] = serializers.Colaborador.Select_encarregado 
serializer_dicts['Select']['atividade'] = serializer_dicts['Select']['tipo_atividade'] 
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def select(request, resource):
    return util.create_select(request, resource, serializer_dicts['Select'])

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def grafico(request, resource):
    graficos_dict = util.get_classes(graficos)
    from django.core.exceptions import ObjectDoesNotExist
    try:
        dados = graficos_dict.get('grafico_' + resource).objects.all().values()
        dados = dados[len(dados) -36:]
        return Response(dados,status=200)
    except ObjectDoesNotExist:
        return Response({'method':'Alerta de pesquisa','message': f'id não encontrada <{id}>' }, status=404)
    
from openpyxl import load_workbook
from django.http import HttpResponse
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def diario_impressao(request):
    obra = models.Obra.objects.get(id=request.GET['cr'])

    colabs = Localizacaoprogramada.objects.all().filter(obra=request.GET['cr'],iniciosemana=request.GET['data'])
        
    arquivo = load_workbook(os.path.join(settings.BASE_DIR, 'template/xlsx/diario.xlsx'))
    aba = arquivo['CONTROLE']
    aba['W2'] = obra.empresa
    aba['W4'] = obra.cidade
    aba['D7'] = obra.descricao
    aba['I9'] = obra.id
    aba['O9'] = obra.orcamento
    # aba['B57'] = obra.etapas or ' '

    tick = 0
    while tick <= 25:
        try:
            aba[f'C{tick + 22}'] = colabs[tick].colaborador
            tick += 1
        except:
            break
            
    # Criar a resposta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=diário.xlsx'

    # Salvar o arquivo no HttpResponse
    arquivo.save(response)

    return response



resources = util.get_resources(models)
resources['atividade']['select'].append('colaborador')
resources['diarioobra']['select'].append('encarregado')
resources['encarregado'] = resources['colaborador']
resources['colaborador']['select'].append('funcao')
resources['localizacaoprogramada']['select'].append('colaborador')
resources['localizacaoprogramada']['select'].append('encarregado')
resources['valor_hora']['select'].append('colaborador')

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def resource(request, name):
    return Response(resources.get(name))


from rest_framework import status
class Colaborador_list(util.LC):
    serializer_class = serializers.Colaborador
    queryset = serializer_class.Meta.model.objects.all().order_by('nome')
    filterset_fields = {
        'demissao': ['isnull'],  # Permite filtrar por isnull e valores exatos
        'nome': ['exact', 'icontains'],       # Exemplo de filtro para nome
        'encarregado': ['exact'],       # Exemplo de filtro para nome
    }
class Colaborador_detail(util.RUD):
    serializer_class = serializers.Colaborador
    queryset = serializer_class.Meta.model.objects.all()
    
    
class Obra_list(util.LC):
    serializer_class = serializers.Obra
    queryset = serializer_class.Meta.model.objects.all().order_by('id')
    filterset_fields = ['finalizada']


class Obra_detail(util.RUD):
    serializer_class = serializers.Obra
    queryset = serializer_class.Meta.model.objects.all()

class Funcao_list(util.LC):
    serializer_class = serializers.Funcao
    queryset = serializer_class.Meta.model.objects.all()
class Funcao_detail(util.RUD):
    serializer_class = Funcao_list.serializer_class
    queryset = serializer_class.Meta.model.objects.all()


class Supervisor_list(util.LC):
    serializer_class = serializers.Supervisor
    queryset = serializer_class.Meta.model.objects.all()
class Supervisor_detail(util.RUD):
    serializer_class = Supervisor_list.serializer_class
    queryset = serializer_class.Meta.model.objects.all()
    
class Atividade_list(util.LC):
    serializer_class = serializers.Atividade
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['colaborador','dia']
class Atividade_detail(util.RUD):
    serializer_class = Atividade_list.serializer_class
    queryset = serializer_class.Meta.model.objects.all()

from rest_framework.parsers import MultiPartParser, FormParser
class Diarioobra_list(util.LC):
    serializer_class = serializers.Diarioobra
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['diario']
    parser_classes = [MultiPartParser, FormParser]

    @util.database_exception
    def create(self, request, *args, **kwargs):
        parametro = request.POST
        if media.upload('diarioobra',request.FILES['file'],parametro.get('imagem')).status_code:
            return super().create(request, *args, **kwargs)
        else: 
            return Response(request,status=status.HTTP_406_NOT_ACCEPTABLE)
class Diarioobra_detail(util.RUD):
    serializer_class = Diarioobra_list.serializer_class
    queryset = serializer_class.Meta.model.objects.all()
    

class Programacao_list(util.LC):
    serializer_class = serializers.Programacao
    queryset = serializer_class.Meta.model.objects.all()

    @util.database_exception
    def create(self, request, *args, **kwargs):
        parametro = json.loads(request.POST.get('parametro'))

        if media.upload('localizacaoprogramada',request.FILES.get('file'),parametro.get('imagem')).status_code:
            for a in json.loads(parametro.get('lanc')):
                a['iniciosemana'] = parametro.get('iniciosemana')
                a['id'] = 'qualquer'
                
                programacao = self.serializer_class(data=a)
                if programacao.is_valid():
                    programacao.save()
                else:
                    media.delete('programacao', parametro.get('imagem'))
                    return Response(programacao.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'sucesso'},status=status.HTTP_201_CREATED) 
        else: 
            return Response(request,status=status.HTTP_406_NOT_ACCEPTABLE)
class Programacao_detail(util.RUD):
    serializer_class = Programacao_list.serializer_class
    queryset = serializer_class.Meta.model.objects.all()


class dia_list(util.LC):
    serializer_class = serializers.Dia
    queryset = serializer_class.Meta.model.objects.all().order_by('-dia')


class ValorHora_list(util.LC):
    serializer_class = serializers.ValorHora
    queryset = serializer_class.Meta.model.objects.all()
class ValorHora_detail(util.RUD):
    serializer_class = ValorHora_list.serializer_class
    queryset = serializer_class.Meta.model.objects.all()