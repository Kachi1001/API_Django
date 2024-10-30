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
from Site_django import media

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
        return Response({'banco de dados': [str(e)]}, status=400)
    else:
        return Response({'method':'Atualizar','message':'Tabela atualizada com sucesso'}, status=200)

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
            'ocupacao': f'muda_cargo({format_sql('id')},{format_sql('data_inicio')},{format_sql('data_fim')},{format_sql('remuneracao')},{format_sql('funcao')})',
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


@api_view(['GET'])
def get_data(request):
    metodo = request.GET.get('metodo')
    id = request.GET.get('parametro')

    obj = dictModels.get(metodo).objects.all()
        
    if metodo in lista_filterColab:
        obj = obj.filter(colaborador=id)
        obj = obj.order_by('-adquirido_em') if 'periodo_aquisitivo' in metodo else obj.order_by('-data_inicio') 
    else: 
        obj = obj.filter(id=id)
        
    obj = list(obj.values())
    if len(obj) == 0:
        return Response({'method':'Alerta de pesquisa','message': f'Em {metodo} não foi possível achar a id  "{id}"' }, status=404)
    else:
        return JsonResponse(obj, safe=False) 
        
    
@api_view(['GET'])
def select(request):
    value = dictModels.get(request.GET.get('metodo')).objects.all().values()
    return Response(value)
    
    
# from . import lembrete as lemb
# @api_view(['GET'])
# def lembrete(request, acao):
#     parametro = request.POST.get('parametro')
#     match acao:
#         case 'toggle':
#             print()
#             # lemb.finalizar(parametro)
#         case 'status':
#             return Response({'status':lemb.status()})
            

from .serializers import *
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import APIException
from django.db import IntegrityError, DatabaseError

# Colaborador
class colaborador_list(generics.ListCreateAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer

class colaborador_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer

@api_view(['POST'])
def colaborador_desligamento(request):
    return funcao(request.data, 'desligamento')
    
# class colaborador_select(generics.ListAPIView):
#     queryset = Colaborador.objects.all()
#     serializer_class = ColaboradorSelect

# Função
class funcao_list(generics.ListCreateAPIView):
    queryset = Funcao.objects.all()
    serializer_class = FuncaoSerializer

class funcao_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Funcao.objects.all()
    serializer_class = FuncaoSerializer
    
    
# Equipe
class equipe_list(generics.ListCreateAPIView):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer

class equipe_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer
    
# 
# Ocupação
class ocupacao_list(generics.ListCreateAPIView):
    queryset = Ocupacao.objects.all().order_by('-data_inicio')
    serializer_class = OcupacaoSerializer
    filterset_fields = ['colaborador']

class ocupacao_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ocupacao.objects.all()
    serializer_class = OcupacaoSerializer
    
from django.shortcuts import get_object_or_404
@api_view(['POST','GET'])
def ocupacao_alterar(request):
    match request.method:
        case 'POST':
            return funcao(request.data, 'dissidio')
        case 'GET':
            queryset = Ocupacao.objects.all()
            return Response(OcupacaoSerializer(get_object_or_404(queryset, pk=request.GET['id'])).data)
            
@api_view(['POST','GET'])
def ocupacao_dissidio(request):
    match request.method:
        case 'POST':
            return funcao(request.data, 'ocupacao')
        case 'GET':
            queryset = Ocupacao.objects.all()
            return Response(OcupacaoSerializer(get_object_or_404(queryset, pk=request.GET['id'])).data)
    
class genericList():
    serializer = None
    
    def get(self, request):
        return Response(self.serializer(self.serializer.Meta.model.objects.all(), many=True).data)
    
#   
# Periodo aquisitivo
class PeriodoAquisitivo_list(generics.ListCreateAPIView):
    serializer_class = PeriodoAquisitivoSerializer
    queryset = PeriodoAquisitivo.objects.all().order_by('-adquirido_em')
    
    filterset_fields = ['colaborador']
    
class PeriodoAquisitivo_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PeriodoAquisitivoSerializer.Meta.model.objects.all()
    serializer_class = PeriodoAquisitivoSerializer
    
@api_view(['POST'])
def PeriodoAquisitivo_funcao(request):
    return funcao(request, 'periodo_aquisitivo')

    
#   
# Ferias processadas
class FeriasProcessadas_list(generics.ListCreateAPIView):
    serializer_class = FeriasProcessadasSerializer
    queryset = FeriasProcessadas.objects.all()
    
    filterset_fields = ['colaborador']

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)

        except DatabaseError as e:
            # Captura outros erros de banco de dados
            return Response(
                {"banco de dados": (str(e).split('CONTEXT')[0])},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class FeriasProcessadas_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeriasProcessadas.objects.all()
    serializer_class = FeriasProcessadasSerializer
    
# 
# Ferias utilizadas
class FeriasUtilizadas_list(generics.ListCreateAPIView):
    serializer_class = FeriasUtilizadasSerializer
    queryset = FeriasUtilizadas.objects.all()
    
    filterset_fields = ['colaborador']
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)

        except DatabaseError as e:
            # Captura outros erros de banco de dados
            return Response(
                {"banco de dados": (str(e).split('CONTEXT')[0])},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

            
class FeriasUtilizadas_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeriasUtilizadas.objects.all()
    serializer_class = FeriasUtilizadasSerializer
    

# Lembrete
class Lembrete_list(generics.ListCreateAPIView):
    queryset = LembreteSerializer.Meta.model.objects.all()
    serializer_class = LembreteSerializer
    
class Lembrete_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LembreteSerializer.Meta.model.objects.all()
    serializer_class = LembreteSerializer

@api_view(['GET'])
def select(request, resource):
    serials = {
        'colaborador': ColaboradorSelect,
        'equipe': EquipeSelect,
        'periodo_aquisitivo': PeriodoAquisitivoSelect,
        'funcao': FuncaoSelect,
        'categoria': [{'value':'1'},{'value':'2'},{'value':'3'},{'value':'TERCEIRO'},{'value':'ESTAGIARIO'}]
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


