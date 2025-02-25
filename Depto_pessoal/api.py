from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import psycopg2
from django.conf import settings
from Site_django import util 
from . import models, views, serializers
retorno200 = Response({'message':'Sucesso'}, status=200)
retorno400 = Response({'message':'Método não encontrado'}, status=400)
retorno404 = Response({'message':'Registro não encontrado'}, status=404)
    
# Configurações de conexão com o banco de dados PostgreSQL
app = __name__.split('.')[0]
db = settings.DATABASES['default']



def funcao_sql(sql): 
    conn = psycopg2.connect(dbname=app, user=db['USER'], password=db['PASSWORD'], host=db['HOST'], port=db['PORT'])
    cursor = conn.cursor()
    print(sql)
    try:
        # Executando a função
        cursor.execute(f"SELECT {sql}")
        conn.commit()
        # Retornando uma resposta de sucesso
    except psycopg2.Error as e:
        e = str(e)
        if 'null value' in e:
            e = f'Campo "{e.split('DETAIL:')[0].split('"')[1]}", não pode ser vazio'
        return Response({'banco de dados': [str(e.split('CONTEXT:')[0])]}, status=400)
    else:
        return Response({'method':'Atualizar','message':'Executado com sucesso com sucesso'}, status=200)

    finally:
        cursor.close()
        conn.close()
        
@permission_classes([IsAuthenticated]) 
def funcao(request, metodo):
    def format_sql(value):
        value = request.get(value)
        if value != None:
            return "'" + str(value) + "'"
        return 'null'
    def bol_sql(value):
        value = request.get(value)
        if value != None:
            return str(value)
        return 'null'
        
    try:
        funcoes = {
            'muda_cargo': f'muda_cargo({format_sql('id')},{format_sql('data_inicio')},{format_sql('data_fim')},{format_sql('remuneracao')},{format_sql('funcao')},{format_sql('terceiro')},{format_sql('equipe')},{format_sql('diaria')},{format_sql('extra')})',  #nova funcao sql
            'dissidio': f'dissidio({format_sql('id')},{format_sql('data_inicio')},{format_sql('remuneracao')})',
            'desligamento': f'desligamento({format_sql('data')},{format_sql('id')})',
        }
        sql = funcoes.get(metodo)
    except:
        return funcao_sql(metodo+'()')

    return funcao_sql(sql)
    
from Site_django.util import generate_serializer_dicts 
Select = {
    'colaborador': serializers.Colaborador.Select,
    'funcao': serializers.Funcao.Select,
    'avaliacao': serializers.TipoAvaliacao.Select,
    'categoria': [{'value':'1'},{'value':'2'},{'value':'3'},{'value':'TERCEIRO'},{'value':'ESTAGIARIO'}],
    'padrao': [{'value':'07:25, 17:55','text':'Colaborador'},{'value':'07:25, 15:25'},{'value':'13:25, 17:25'}],
}    
serializer_dicts = generate_serializer_dicts(serializers)
Select.update(serializer_dicts['Select'])
serializer_dicts['Table']['colaborador'] = serializer_dicts['Table']['colaborador_']

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def select(request, resource):
    return util.create_select(request, resource, Select)
table_models = util.get_classes(models)
table_views = util.get_classes(views)
table_models['colaborador'] = table_models['colaborador_']
table_models['avaliacao'] = table_models['colaborador_']
   
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tabela_list(request): 
    result = {'tabelas':table_models.keys(),'view':table_views.keys()}
    return Response(result)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tabela(request, table):
    dicts = table_models
    dicts.update(table_views)
    return util.get_table(request, table, dicts, serializer_dicts['Table'])

resources = util.get_resources(models)
resources['colaborador'] = resources['colaborador_']
resources['avaliacao'] = resources['colaborador_']
resources['funcao'] = resources['funcao_']
resources['funcao']['select'].append('categoria')
resources['ponto'] = resources['lembrete'] 
resources['ponto']['select'].append('padrao') 
resources['desligamento'] = {'text':['data', 'id']}
resources['integracao']['select'].append('obra')
resources['gera_calendario'] = {'text':['data']}
resources['integracao_epi'] = resources['integracao_aso']
resources['readmissao'] = {'text':['id','colaborador','data_inicio','remuneracao','diaria'],'check':['terceiro','extra'],'select':['funcao','equipe']}
@api_view(['GET'])
def resource(request, name):
    return Response(resources.get(name))

graficos = {
    'rotatividade': views.ativos_rotatividade,
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
class colaborador_list(util.LC):
    serializer_class = serializers.Colaborador
    queryset = serializer_class.Meta.model.objects.all()

class colaborador_detail(util.RUD):
    serializer_class = serializers.Colaborador
    queryset = serializer_class.Meta.model.objects.all()

    @util.database_exception
    def destroy(self, request, *args, **kwargs):
        return funcao(request.data, 'desligamento')
        # return super().destroy(request, *args, **kwargs)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def colaborador_desligamento(request):
    return funcao(request.data, 'desligamento')
    
# class colaborador_select(generics.ListAPIView):
#     queryset = Colaborador.objects.all()
#     serializer_class = ColaboradorSelect

# Função
class funcao_list(util.LC):
    serializer_class = serializers.Funcao
    queryset = serializer_class.Meta.model.objects.all()


class funcao_detail(util.RUD):
    serializer_class = serializers.Funcao
    queryset = serializer_class.Meta.model.objects.all()
    
    
# Equipe
class equipe_list(util.LC):
    serializer_class = serializers.Equipe
    queryset = serializer_class.Meta.model.objects.all()

class equipe_detail(util.RUD):
    serializer_class = serializers.Equipe
    queryset = serializer_class.Meta.model.objects.all()
    
# 
# Ocupação
class ocupacao_list(util.LC):
    serializer_class = serializers.Ocupacao
    queryset = serializer_class.Meta.model.objects.all().order_by('-data_inicio')
    filterset_fields = ['colaborador','id']

class ocupacao_detail(util.RUD):
    serializer_class = serializers.Ocupacao
    queryset = serializer_class.Meta.model.objects.all()
    
    
from django.shortcuts import get_object_or_404
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated]) 
def ocupacao_alterar(request):
    serializer = serializers.Ocupacao
    match request.method:
        case 'POST':
            return funcao(request.data, 'muda_cargo')
        case 'GET':
            queryset = serializer.Meta.model.objects.all()
            return Response(serializer(get_object_or_404(queryset, pk=request.GET['id'])).data)
            
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated]) 
def ocupacao_dissidio(request):
    serializer = serializers.Ocupacao
    match request.method:
        case 'POST':
            return funcao(request.data, 'dissidio')
        case 'GET':
            queryset = serializer.Meta.model.objects.all()
            return Response(serializer(get_object_or_404(queryset, pk=request.GET['id'])).data)
    
#   
# Periodo aquisitivo
class PeriodoAquisitivo_list(util.LC):
    serializer_class = serializers.PeriodoAquisitivo
    queryset = serializer_class.Meta.model.objects.all().order_by('-adquirido_em')
    filterset_fields = ['colaborador']
    
    
class PeriodoAquisitivo_detail(util.RUD):
    serializer_class = serializers.PeriodoAquisitivo
    queryset = serializer_class.Meta.model.objects.all()
    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def PeriodoAquisitivo_funcao(request):
    return funcao(request, 'periodo_aquisitivo')

    
#   
# Ferias processadas
class FeriasProcessadas_list(util.LC):
    serializer_class = serializers.FeriasProcessadas
    queryset = serializer_class.Meta.model.objects.all().order_by('-id')
    filterset_fields = ['colaborador']
class FeriasProcessadas_detail(util.RUD):
    serializer_class = serializers.FeriasProcessadas
    queryset = serializer_class.Meta.model.objects.all()
# 
# Ferias utilizadas
class FeriasUtilizadas_list(util.LC):
    serializer_class = serializers.FeriasUtilizadas
    queryset = serializer_class.Meta.model.objects.all().order_by('-id')
    filterset_fields = ['colaborador']
class FeriasUtilizadas_detail(util.RUD):
    serializer_class = serializers.FeriasUtilizadas
    queryset = serializer_class.Meta.model.objects.all()

# Lembrete
from rest_framework.permissions import IsAuthenticatedOrReadOnly
class Lembrete_list(util.LC):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.Lembrete
    queryset = serializer_class.Meta.model.objects.all()
        
class Lembrete_detail(util.RUD):
    serializer_class = serializers.Lembrete
    queryset = serializer_class.Meta.model.objects.all()

# Feriado
class Feriado_list(util.LC):
    serializer_class = serializers.Feriado
    queryset = serializer_class.Meta.model.objects.all()
        
class Feriado_detail(util.RUD):
    serializer_class = serializers.Feriado
    queryset = serializer_class.Meta.model.objects.all()

    
class TipoAvaliacao():
    serializer_class = serializers.TipoAvaliacao
    queryset = serializer_class.Meta.model.objects.all()

class TipoAvaliacao_list(TipoAvaliacao,util.LC):
    pass
    
class TipoAvaliacao_detail(TipoAvaliacao,util.RUD):
    pass
    

        
from django.core.cache import cache
        
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated]) 
def app_menu(request, app):
    base = f'Depto_pessoal:app:{app}:'
    status = 200
    if request.method == 'POST':
        ca = cache.get(f'{base}toggle')
        ca = not bool(ca)
        cache.set(f'{base}toggle', int(ca), None)
        status = 202
    values = cache.get_many([f'{base}run',f'{base}toggle',f'{base}updated'])
    return Response(values,status=status)
        
@api_view(['GET'])
def app_feriado(request):
    try: feriados = models.Feriado.objects.get(id=util.get_hoje())
    except: return Response(0)
    else: return Response(1)

class IntegracaoNr_list(util.LC):
    serializer_class = serializers.IntegracaoNr
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['colaborador','id']
class IntegracaoNr_detail(util.RUD):
    serializer_class = serializers.IntegracaoNr
    queryset = serializer_class.Meta.model.objects.all()
    
class IntegracaoNrTipo_list(util.LC):
    serializer_class = serializers.IntegracaoNrTipo
    queryset = serializer_class.Meta.model.objects.all()
class IntegracaoNrTipo_detail(util.RUD):
    serializer_class = serializers.IntegracaoNrTipo
    queryset = serializer_class.Meta.model.objects.all()
    
class Integracao_list(util.LC):
    serializer_class = serializers.Integracao
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['colaborador','id']
class Integracao_detail(util.RUD):
    serializer_class = serializers.Integracao
    queryset = serializer_class.Meta.model.objects.all()
    
class IntegracaoEpi_list(util.LC):
    serializer_class = serializers.IntegracaoEpi
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['colaborador','id']

class IntegracaoEpi_detail(util.RUD):
    serializer_class = serializers.IntegracaoEpi
    queryset = serializer_class.Meta.model.objects.all()
    
# Feriado
class Lembrete(util.LC):
    serializer_class = serializers.Lembrete
    queryset = serializer_class.Meta.model.objects.all()
        
class Insalubridade_list(util.LC):
    serializer_class = serializers.Insalubridade
    queryset = serializer_class.Meta.model.objects.all()
class Insalubridade_detail(util.RUD):
    serializer_class = serializers.Insalubridade
    queryset = serializer_class.Meta.model.objects.all()

    
from openpyxl import load_workbook
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def HorasPonto_import(request):
        arquivo = load_workbook(request.FILES['file'])
        try:
            tabela = arquivo['Relatório xlsx']
        except KeyError as e:
            return Response({'Arquivo':'Arquivo não compatível!','detalhe':str(e)}, status=406)
        colabs = {}
        for colab in models.Colaborador.objects.all().values():
            colabs[colab.get('nome')] = colab.get('id')

        conflito = []
        linha = 2
        while tabela[f'A{linha}'].value and tabela[f'A{linha}'].value != 'Resumo':
            colab = tabela[f'A{linha}'].value
            if not (colab in colabs) and not (colab in conflito):
                conflito.append(colab)
            linha += 1
            
        if len(conflito) > 0:
            result = {}
            for x in conflito:
                result[x] = 'Colaborador não encontrado!'
            return Response(result, status=406)
        
        limite = linha
        linha = 2
        while linha < limite:
            try:    
                data = datetime.strptime(tabela[f'B{linha}'].value.split(', ')[1], '%d/%m/%Y')
                queryset_colab = models.Colaborador.objects.all()
                colab = queryset_colab.get(id = colabs.get(tabela[f'A{linha}'].value))
                lanc = models.HorasPonto.objects.create(colaborador=colab, extras=tabela[f'H{linha}'].value, data=data)        
            except Exception as e:
                print(e)
                return Response({'Erro': f'Erro ao adicionar no banco, linha: {linha}'}, status=400)
            linha += 1 
        return Response({'Sucesso':'Importado com sucesso!'}, status=203)            

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
@util.database_exception 
def GeraCalendario(request):
    def format_sql(value):
        value = request.data.get(value)
        if value:
            return "'" + str(value) + "'"
        return 'null'
    if format_sql('data') == 'null':
        return Response({'DATA':'Este campo não pode ser nulo!'}, 500)
    return funcao_sql(f'gera_calendario {format_sql('data')}')  
    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
@util.database_exception 
def ReAdmitir(request):
    data = request.data
    resource = resources['readmissao']
    def format_sql(value):
        value = request.data.get(value)
        if value:
            return "'" + str(value) + "'"
        return 'null'   
    def format_bool(value):
        value = request.data.get(value)
        if value != None:
            return str(value)
        return 'null'
    result = {}
    campos = resource.get('text') + resource.get('select') + resource.get('check')
    for x in campos:
        if data.get(x) == None:
            result[x.upper()] = 'Este campo não pode ser nulo!'
    if len(result) > 0:
        return Response(result, 500)
    return funcao_sql(f'readmissao ({format_sql('id')},{format_sql('data_inicio')},{format_sql('remuneracao')},{format_sql('funcao')},{format_bool('terceiro')},{format_sql('equipe')},{format_sql('diaria')},{format_bool('extra')})')  