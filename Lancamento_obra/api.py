import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
import psycopg2
from django.conf import settings
from .models import *
from .views import *
import json
from django.http import JsonResponse
from .mani import *
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
def funcao(request, funcao):
    def get_formatter(value, padrao= None):
        value = parametro.get(value, padrao)
        if value != None:
            return "'" + str(value) + "'"
        return 'null'
        
    funcao_void = ['atualizar_tabelas',]
    if funcao in funcao_void:
        return funçãoSQL(funcao+'()')
    parametro = request.data
    if funcao == 'efetividade':
        return funçãoSQL(f"get_efetividade({get_formatter('colaborador')},{get_formatter('obra')},{get_formatter("dataini")},{get_formatter("datafim")})")
    elif funcao == 'subconsulta_lancamento':
        return funçãoSQL(f"{funcao}('{parametro.get("colaborador", '')}','{parametro.get("dia", '2050-01-01')}')")



dictModels = {
    'funcao': Funcao,
    'diario': Diarioobra,
    'obra': Obra,
    'programacao': Localizacaoprogramada,
    'atividade': Atividade,
    'supervisor': Supervisor,
    'funcao': Funcao,
    'colaborador': Colaborador,
    'descontos_resumo': DescontosResumo,
    'diarias':Diarias,
    'efetividade':Efetividade,
    # 'hora_mes':HoraMes,
    'incompletos':Incompletos,
    'fechados': Tecnicon,
    'alocacoes': Alocacoes,
}
from . import models, views
table_models = util.get_classes(models)
table_views = util.get_classes(views)
@api_view(['GET'])
def tabela(request, table):
    dicts = table_models
    dicts.update(table_views)
    return util.get_table(request, table, dicts)

@api_view(['GET'])
def get_data(request):
    metodo = request.GET.get('metodo')
    id = request.GET.get('parametro')
    if metodo == 'diario':
        obj = Diarioobra.objects.all().filter(diario=id)
    elif metodo == 'lanc_dia':
        colab = request.GET.get('colaborador').replace('%20', ' ')
        obj = Atividade.objects.all().filter(colaborador=colab,dia=request.GET.get('dia'))
    else:
        obj = dictModels.get(metodo).objects.all().filter(id=id)
    
    value = list(obj.values())

    if len(value) == 0:
        return Response({'method':'Alerta de pesquisa','message': f'id não encontrada " {id}"' }, status=404)
    else:
        return JsonResponse(value, safe=False) 
    
@api_view(['GET'])
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
    
from openpyxl import load_workbook
from django.http import HttpResponse
@api_view(['GET'])
def diario_impressao(request):
    obra = Obra.objects.get(id=request.GET['cr'])

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

@api_view(['GET'])
def select(request, resource):
    from .serializers import Select

    return util.create_select(request, resource, Select)

resources = util.get_resources(models)
resources['atividade']['select'].append('colaborador')
resources['diarioobra']['select'].append('encarregado')
resources['encarregado'] = resources['colaborador']
resources['colaborador']['select'].append('funcao')

@api_view(['GET'])
def resource(request, name):
    return Response(resources.get(name))


from rest_framework import generics, status
class Colaborador_list(util.LC):
    serializer_class = ColaboradorSerializer
    queryset = ColaboradorSerializer.Meta.model.objects.all().order_by('nome')
    filterset_fields = {
        'demissao': ['isnull'],  # Permite filtrar por isnull e valores exatos
        'nome': ['exact', 'icontains'],       # Exemplo de filtro para nome
        'encarregado': ['exact'],       # Exemplo de filtro para nome
    }

    
class Colaborador_detail(util.RUD):
    serializer_class = ColaboradorSerializer
    queryset = ColaboradorSerializer.Meta.model.objects.all()
    
    
class Obra_list(util.LC):
    serializer_class = ObraSerializer
    queryset = serializer_class.Meta.model.objects.all().order_by('id')
    filterset_fields = ['finalizada']


class Obra_detail(util.RUD):
    serializer_class = ObraSerializer
    queryset = serializer_class.Meta.model.objects.all()
    
class Funcao():
    serializer_class = FuncaoSerializer
    queryset = serializer_class.Meta.model.objects.all()

class Funcao_list(Funcao, util.LC):
    pass

class Funcao_detail(Funcao, util.RUD):
    pass

class Supervisor():
    serializer_class = SupervisorSerializer
    queryset = serializer_class.Meta.model.objects.all()

class Supervisor_list(Supervisor, util.LC):
    pass

class Supervisor_detail(Supervisor, util.RUD):
    pass    
    
class Atividade_list(util.LC):
    serializer_class = AtividadeSerializer
    queryset = serializer_class.Meta.model.objects.all()


class Atividade_detail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AtividadeSerializer
    queryset = serializer_class.Meta.model.objects.all()
    
    @util.database_exception
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs) 
    
    @util.database_exception
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
class Diarioobra_list(util.LC):
    serializer_class = DiarioobraSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['diario']
    
    @util.database_exception
    def create(self, request, *args, **kwargs):
        parametro = json.loads(request.POST.get('parametro'))
        
        if media.upload('diarioobra',request.FILES.get('file'),parametro.get('imagem')).status_code:
            diario = DiarioobraSerializer(data=parametro)
            if diario.is_valid():
                diario.save()
                return Response(diario.data,status=status.HTTP_201_CREATED) 
            else:
                media.delete('diario', parametro.get('imagem'))
                return Response(diario.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
        else: 
            return Response(request,status=status.HTTP_406_NOT_ACCEPTABLE)
            
    
class Diarioobra_detail(util.RUD):
    serializer_class = DiarioobraSerializer
    queryset = serializer_class.Meta.model.objects.all()
    

class Programacao_list(util.LC):
    serializer_class = ProgramacaoSerializer
    queryset = serializer_class.Meta.model.objects.all()

    @util.database_exception
    def create(self, request, *args, **kwargs):
        parametro = json.loads(request.POST.get('parametro'))

        if media.upload('programacao',request.FILES.get('file'),parametro.get('imagem')).status_code:
            for a in json.loads(parametro.get('lanc')):
                a['iniciosemana'] = parametro.get('iniciosemana')
                a['id'] = 'qualquer'
                
                programacao = ProgramacaoSerializer(data=a)
                if programacao.is_valid():
                    programacao.save()
                else:
                    media.delete('programacao', parametro.get('imagem'))
                    return Response(programacao.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'sucesso'},status=status.HTTP_201_CREATED) 
        else: 
            return Response(request,status=status.HTTP_406_NOT_ACCEPTABLE)
        
class Programacao_detail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProgramacaoSerializer
    queryset = serializer_class.Meta.model.objects.all()
