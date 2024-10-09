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
from Midia.api import upload

retorno200 = Response({'message':'Sucesso'}, status=200)
retorno400 = Response({'message':'Método não encontrado'}, status=400)
retorno404 = Response({'message':'Registro não encontrado'}, status=404)
    
# Configurações de conexão com o banco de dados PostgreSQL
app = __name__.split('.')[0]
db = settings.DATABASES['default']

def funçãoSQL(funcao): 
    conn = psycopg2.connect(dbname=app, user=db['USER'], password=db['PASSWORD'], host=db['HOST'], port=db['PORT'])
    cursor = conn.cursor()

    try:
        # Executando a função
        cursor.execute(f"SELECT {funcao}")
        conn.commit()
        # Retornando uma resposta de sucesso
    except psycopg2.Error as e:
        return Response({'method':'Erro do banco de dados','message': str(e)}, status=400)
    else:
        return Response({'method':'Atualizar','message':'Tabela atualizada com sucesso'}, status=200)

    finally:
        cursor.close()
        conn.close()
        

@api_view(['POST'])
def funcao(request):
    def formatSQL(value, padrao):
        value = parametro.get(value, padrao)
        if value != None:
            return "'" + str(value) + "'"
        return 'null'

    metodo = request.POST.get('metodo')
    try:
        parametro = json.loads(request.POST.get('parametro'))
        funcao = {
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
    parametro = request.GET.get('parametro')
    value = None
    metodos = {
        'select': {
            'equipe': Equipe.objects.all().values(),
            'categoria': [{'value':'1'},{'value':'2'},{'value':'3'},{'value':'ESTAGIARIO'},{'value':'DIRETOR'},{'value':'TERCEIRO'}]            
        },
        'table': {
            'funcao': Funcao.objects.all().values(),
            'equipe': Equipe.objects.all().values('id')
        } 
    }
    value = metodos.get(metodo).get(parametro)

    if value == None:
        return Response({'method':'Tabela','message':'Método não encontrado'}, status=400)
    else:
        return JsonResponse(list(value), safe=False) 
   
@api_view(['GET'])
def tabela(request, table): 
    return JsonResponse(buildTable(request, table, dictModels.get(table).objects.all()), safe=False)

lista_filterColab = []

for x in ['ferias_processadas','ferias_utilizadas','periodo_aquisitivo','ocupacao']:
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