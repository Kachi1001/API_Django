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
        

@api_view(['POST'])
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
            'ocupacao': f'muda_cargo({formatSQL('id')},{formatSQL('data_inicio')},{formatSQL('remuneracao')},{formatSQL('funcao_id')})',
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
            'equipe': Equipe.objects.all().values('id'),
            'categoria': [{'value':'1'},{'value':'2'},{'value':'3'},{'value':'ESTAGIARIO'},{'value':'DIRETOR'},{'value':'TERCEIRO'}],   
            'colaborador': Colaborador.objects.all().values('id').order_by('id'),
            'funcao_id': Funcao.objects.all().values().order_by('id'),
            'periodo_aquisitivo_id': PeriodoAquisitivo.objects.all().values().order_by('id'),
 
        },
        'table': {
            'funcao': Funcao.objects.all().values().order_by('id'),
            'equipe': Equipe.objects.all().values('id').order_by('id')
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
    
    
# from . import lembrete as lemb
# @api_view(['POST'])
# def lembrete(request, acao):
#     parametro = request.POST.get('parametro')
#     match acao:
#         case 'iniciar':
#             lemb.iniciar(parametro)
#         case 'finalizar':
#             lemb.finalizar(parametro)
#         case 'status':
#             lemb.status(parametro)