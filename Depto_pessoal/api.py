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

def funçãoSQL(funcao): 
    conn = psycopg2.connect(dbname=app, user=db['USER'], password=db['PASSWORD'], host=db['HOST'], port=db['PORT'])
    cursor = conn.cursor()
    print(funcao)
    try:
        # Executando a função
        cursor.execute(f"SELECT {funcao}")
        conn.commit()
        # Retornando uma resposta de sucesso
    except psycopg2.Error as e:
        e = str(e)
        if 'null value' in e:
            e = f'Campo "{e.split('DETAIL:')[0].split('"')[1]}", não pode ser vazio'
        return Response({'method':'Erro do banco de dados','message': str(e)}, status=400)
    else:
        return Response({'method':'Atualizar','message':'Tabela atualizada com sucesso'}, status=200)

    finally:
        cursor.close()
        conn.close()
        

def funcao(request):
    def formatSQL(value, padrao = None):
        value = parametro.get(value, padrao)
        if value != None:
            return "'" + str(value) + "'"
        return 'null'

    metodo = request.POST.get('metodo')
    try:
        parametro = json.loads(request.POST.get('parametro'))
        funcao = {
            'ocupacao': f'muda_cargo({formatSQL('id')},{formatSQL('data_inicio')},{formatSQL('data_fim')},{formatSQL('remuneracao')},{formatSQL('funcao_id')})',
            'dissidio': f'dissidio({formatSQL('id')},{formatSQL('data_inicio')},{formatSQL('remuneracao')})',
            'desligamento': f'desligamento({formatSQL('data')},{formatSQL('id')})',
        }
    except:
        return funçãoSQL(metodo+'()')
    else:
        return funçãoSQL(funcao.get(metodo))

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

@api_view(['POST'])
def register(request):
    parametro = json.loads(request.POST.get('parametro'))
    metodo = request.POST.get('metodo')
    obj = dictModels.get(metodo)

    return mani.create(parametro,obj())
    
@api_view(['PATCH'])
def update(request):
    metodo = request.POST.get('metodo')
    parametro = json.loads(request.POST.get('parametro'))
    owner = request.POST.get('user')
    obj = dictModels.get(metodo).objects.get(pk=parametro.get('id'))
    return mani.update(parametro,obj)
          
    
    
        
@api_view(['PUT'])
def deletar(request):
    metodo = request.POST.get('metodo')
    id = request.POST.get('parametro')
    owner = request.POST.get('user')
    try:
        obj = dictModels.get(metodo).objects.get(id=id)
        obj.delete()
    except ObjectDoesNotExist as e:
        return Response({'method': 'Delete','message':'Item não encontrado'}, status=400)
    else:
        return Response({'method':'Delete','message':f'{id}, foi deletado com sucesso'})
@api_view(['DELETE'])
def deletar(request):
    metodo = request.POST.get('metodo')
    id = request.POST.get('parametro')
    owner = request.POST.get('user')
    try:
        obj = dictModels.get(metodo).objects.get(id=id)
        obj.delete()
    except ObjectDoesNotExist as e:
        return Response({'method': 'Delete','message':'Item não encontrado'}, status=400)
    else:
        return Response({'method':'Delete','message':f'{id}, foi deletado com sucesso'})
      
@api_view(['GET'])
def get_list(request):
    metodo = request.GET.get('metodo')
    parametro = request.GET.get('parametro', None)
    value = None
    metodos = {
            'equipe': Equipe.objects.all().values('id'),
            'categoria': [{'value':'1'},{'value':'2'},{'value':'3'},{'value':'ESTAGIARIO'},{'value':'DIRETOR'},{'value':'TERCEIRO'}],   
            'colaborador': Colaborador.objects.all().values('id').order_by('id'),
            'funcao_id': Funcao.objects.all().values().order_by('id'),
            'periodo_aquisitivo_id': PeriodoAquisitivo.objects.all().values().order_by('id'),
            'padrao': [
                {'text':'Colaborador [7:25, 17:55] ', 'value':'7:25, 17:55'},
                {'text':'Aprendiz [13:25, 17:25]', 'value':'13:25, 17:25'},
                {'text':'Estagiário [7:25, 13:25]', 'value':'7:25, 13:25'},
            ],
            'funcao': Funcao.objects.all().values().order_by('id'),
            'equipe': Equipe.objects.all().values('id').order_by('id'),
    }
    value = metodos.get(metodo)
    if parametro:
        # Divide a string no formato 'campo=valor'
        campo, valor = filter.split('=')

        # Cria um dicionário com o filtro dinâmico
        filtro_dinamico = {campo: valor}

        # Aplica o filtro na ORM do Django
        value = value.objects.filter(**filtro_dinamico)
        
    if value == None:
        return Response({'method':'Tabela','message':'Método não encontrado'}, status=400)
    else:
        return JsonResponse(list(value), safe=False) 
   
@api_view(['GET'])
def tabela(request, table): 
    return JsonResponse(buildTable(request, table, dictModels.get(table).objects.all()), safe=False)

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
    
    
from . import lembrete as lemb
@api_view(['GET'])
def lembrete(request, acao):
    parametro = request.POST.get('parametro')
    match acao:
        case 'toggle':
            print()
            # lemb.finalizar(parametro)
        case 'status':
            return Response({'status':lemb.status()})
            

from .serializers import *
from rest_framework import generics, viewsets

class colaborador_list(generics.ListCreateAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer

class colaborador_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer


# Função
class funcao_list(generics.ListCreateAPIView):
    queryset = Funcao.objects.all()
    serializer_class = FuncaoSerializer

class funcao_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Funcao.objects.all()
    serializer_class = FuncaoSerializer


# Ocupação
class ocupacao_list(generics.ListCreateAPIView):
    queryset = Ocupacao.objects.all()
    serializer_class = OcupacaoSerializer

class ocupacao_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ocupacao.objects.all()
    serializer_class = OcupacaoSerializer
    
@api_view(['POST'])
def ocupacao_alterar(request, pk):
    fu
                
@api_view(['POST'])
def ocupacao_disidio(request, pk):
    try:
        resource = Ocupacao.objects.get(pk=pk)
    except:
        return Response(status=204)
    else:
        pass
    
# Ferias processadas
class FeriasProcessadas_list(viewsets.ViewSet):
    def get(self, request):
        queryset = FeriasProcessadasSerializer.Meta.model.objects.all()
        serializer = FeriasProcessadasSerializer(queryset)
        return Response(serializer.data)
    def post(self, request):
        pass
    
class FeriasProcessadas_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeriasProcessadas.objects.all()
    serializer_class = FeriasProcessadasSerializer

# Ferias utilizadas
class FeriasUtilizadas_list(viewsets.ViewSet):
    def get(self, request):
        queryset = FeriasUtilizadas.objects.all()
        serializer = FeriasUtilizadasSerializer(queryset)
        return Response(serializer.data)
    def post(self, request):
        pass
    
class FeriasUtilizadas_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeriasUtilizadas.objects.all()
    serializer_class = FeriasUtilizadasSerializer
    
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


