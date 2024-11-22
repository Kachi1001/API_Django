from rest_framework.decorators import api_view
from rest_framework.response import Response
import psycopg2
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import *
import json
from django.http import JsonResponse
from .mani import mani
from .tables import buildTable
from Site_django import util 

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
        

def funcao(request, metodo):
    def format_sql(value):
        value = request.get(value)
        if value != None:
            return "'" + str(value) + "'"
        return 'null'

    try:
        funcoes = {
            'muda_cargo': f'muda_cargo({format_sql('id')},{format_sql('data_inicio')},{format_sql('data_fim')},{format_sql('remuneracao')},{format_sql('funcao')})',
            'dissidio': f'dissidio({format_sql('id')},{format_sql('data_inicio')},{format_sql('remuneracao')})',
            'desligamento': f'desligamento({format_sql('data')},{format_sql('id')})',
        }
        sql = funcoes.get(metodo)
    except:
        return funcao_sql(metodo+'()')

    return funcao_sql(sql)

dictModels = {
    'funcao': Funcao,
    'colaborador': Colaborador,
    'equipe': Equipe,
    'periodo_aquisitivo': PeriodoAquisitivo,
    'ferias_utilizadas': FeriasUtilizadas,
    'ferias_processadas': FeriasProcessadas,
    'ocupacao': Ocupacao,
    'lembrete': Lembrete,
}

   
@api_view(['GET'])
def tabela(request, table): 
    return Response(buildTable(request, table, dictModels.get(table).objects.all()))

lista_filterColab = ['historico_ocupacao']

for x in ['ferias_processadas','ferias_utilizadas','periodo_aquisitivo']:
    new = 'historico_'+x
    lista_filterColab.append(x)
    lista_filterColab.append(new)
    dictModels[new] = dictModels[x]
    

            
from .serializers import *


# Colaborador
class colaborador_list(util.LC):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer


class colaborador_detail(util.RUD):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer
    
    def destroy(self, request, *args, **kwargs):
        return funcao(request.data, 'desligamento')
        # return super().destroy(request, *args, **kwargs)
    
@api_view(['POST'])
def colaborador_desligamento(request):
    return funcao(request.data, 'desligamento')
    
# class colaborador_select(generics.ListAPIView):
#     queryset = Colaborador.objects.all()
#     serializer_class = ColaboradorSelect

# Função
class funcao_list(util.LC):
    queryset = Funcao.objects.all()
    serializer_class = FuncaoSerializer

class funcao_detail(util.RUD):
    queryset = Funcao.objects.all()
    serializer_class = FuncaoSerializer
    
    
# Equipe
class equipe_list(util.LC):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer

class equipe_detail(util.RUD):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer
    
# 
# Ocupação
class ocupacao_list(util.LC):
    queryset = Ocupacao.objects.all().order_by('-data_inicio')
    serializer_class = OcupacaoSerializer
    filterset_fields = ['colaborador','id']

class ocupacao_detail(util.RUD):
    queryset = Ocupacao.objects.all()
    serializer_class = OcupacaoSerializer
    
from django.shortcuts import get_object_or_404
@api_view(['POST','GET'])
def ocupacao_alterar(request):
    match request.method:
        case 'POST':
            return funcao(request.data, 'muda_cargo')
        case 'GET':
            queryset = Ocupacao.objects.all()
            return Response(OcupacaoSerializer(get_object_or_404(queryset, pk=request.GET['id'])).data)
            
@api_view(['POST','GET'])
def ocupacao_dissidio(request):
    match request.method:
        case 'POST':
            return funcao(request.data, 'dissidio')
        case 'GET':
            queryset = Ocupacao.objects.all()
            return Response(OcupacaoSerializer(get_object_or_404(queryset, pk=request.GET['id'])).data)
    
class genericList():
    serializer = None
    
    def get(self, request):
        return Response(self.serializer(self.serializer.Meta.model.objects.all(), many=True).data)
    
#   
# Periodo aquisitivo
class PeriodoAquisitivo_list(util.LC):
    serializer_class = PeriodoAquisitivoSerializer
    queryset = PeriodoAquisitivo.objects.all().order_by('-adquirido_em')
    
    filterset_fields = ['colaborador']
    
class PeriodoAquisitivo_detail(util.RUD):
    queryset = PeriodoAquisitivoSerializer.Meta.model.objects.all()
    serializer_class = PeriodoAquisitivoSerializer
    
@api_view(['POST'])
def PeriodoAquisitivo_funcao(request):
    return funcao(request, 'periodo_aquisitivo')

    
#   
# Ferias processadas
class FeriasProcessadas_list(util.LC):
    serializer_class = FeriasProcessadasSerializer
    queryset = FeriasProcessadas.objects.all()
    
    filterset_fields = ['colaborador']

            
class FeriasProcessadas_detail(util.RUD):
    queryset = FeriasProcessadas.objects.all()
    serializer_class = FeriasProcessadasSerializer

# 
# Ferias utilizadas
class FeriasUtilizadas_list(util.LC):
    serializer_class = FeriasUtilizadasSerializer
    queryset = FeriasUtilizadas.objects.all()
    
    filterset_fields = ['colaborador']
            
class FeriasUtilizadas_detail(util.RUD):
    queryset = FeriasUtilizadas.objects.all()
    serializer_class = FeriasUtilizadasSerializer
    

# Lembrete
class Lembrete_list(util.LC):
    serializer_class = LembreteSerializer
    queryset = serializer_class.Meta.model.objects.all()
        
class Lembrete_detail(util.RUD):
    serializer_class = LembreteSerializer    
    queryset = serializer_class.Meta.model.objects.all()

# Feriado
class Feriado_list(util.LC):
    serializer_class = FeriadoSerializer
    queryset = serializer_class.Meta.model.objects.all()
        
class Feriado_detail(util.RUD):
    serializer_class = FeriadoSerializer    
    queryset = serializer_class.Meta.model.objects.all()

@api_view(['GET'])
def select(request, resource):
    serials = {
        'colaborador': ColaboradorSelect,
        'equipe': EquipeSelect,
        'periodo_aquisitivo': PeriodoAquisitivoSelect,
        'funcao': FuncaoSelect,
        'categoria': [{'value':'1'},{'value':'2'},{'value':'3'},{'value':'TERCEIRO'},{'value':'ESTAGIARIO'}],
        'padrao': [{'value':'07:25, 17:55','text':'Colaborador'},{'value':'07:25, 15:25'},{'value':'13:25, 17:25'}],
    }
    if resource in serials:
        serial = serials.get(resource)
    else:
        return Response({'method':'Select','message':'Campo não encontrado na API'},status=404)
    
    try:
        values = serial(serial.Meta.model.objects.all(), many= True).data
    except:
        values = serial
    
    return Response(values)
        
from django.core.cache import cache
        
@api_view(['POST','GET'])
def app_menu(request):
    base = 'Depto_pessoal:app:'
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
    try: feriados = Feriado.objects.get(id=util.get_hoje)
    except Feriado.DoesNotExist: return 0
    else: return 1
# @api_view(['GET','PUT', 'DELETE'])
# def colaborador(request, pk):
#     try:
#         colaborador = Colaborador.objects.get(pk=pk)
#     except:
#         return Response(status=204)
#     else:
    
#         match request.method:
#             case 'GET':
#                 serializer = ColaboradorSerializer(colaborador)
#                 return Response(serializer.data)
#             case 'PUT':
#                 serializer = ColaboradorSerializer(colaborador, data=request.data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data)
#                 return Response(serializer.errors, status=400)
#             case 'DELETE':
#                 colaborador.delete()
#                 return Response(status=200)

