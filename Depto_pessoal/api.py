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
dbname = 'Lancamento_obra'
user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
host = settings.DATABASES['default']['HOST']
port = settings.DATABASES['default']['PORT']


def funçãoSQL(funcao): 
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    print(funcao)
    try:
        # Executando a função
        cursor.execute(f"SELECT {funcao}")
        conn.commit()
        # Retornando uma resposta de sucesso
    except psycopg2.Error as e:
        return Response({'error': str(e)}, status=400)
    else:
        return Response({'method':'Atualizar','message':'Tabela atualizada com sucesso'}, status=200)

    finally:
        cursor.close()
        conn.close()
        

@api_view(['GET'])
def funcao(request):
    funcao_void = ['atualizar_tabelas',]
    metodo = request.GET.get('metodo')
    if metodo in funcao_void:
        return funçãoSQL(metodo+'()')

    parametro = json.loads(request.GET.get('parametro'))
    if metodo == 'efetividade':
        func = f"get_efetividade('{parametro.get("colaborador", '')}','{parametro.get("obra" , '')}','{parametro.get("dataini", '2000-01-01')}','{parametro.get("datafim", '2050-01-01')}')"
        return funçãoSQL(func)
    elif metodo == 'subconsulta_lancamento':
        return funçãoSQL(f"{metodo}('{parametro.get("colaborador", '')}','{parametro.get("dia", '2050-01-01')}')")
    return retorno400



dictModels = {
    'funcao': Funcao,
    'colaborador': Colaborador,
    'equipe': Equipe

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
    if metodo == 'supervisor':
        obj = Supervisor.objects.get(supervisor=parametro.get('supervisor'))
    else:
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
def grafico(request):
    metodo = request.GET.get('metodo')
    result = retorno400
    try:
        if metodo == 'grafico1':
            return Response(Graficos.objects.all().values('mes','hora_50','hora_100'),status=200)
    except ObjectDoesNotExist:
            return Response({'method':'Alerta de pesquisa','message': f'id não encontrada <{id}>' }, status=404)
    
@api_view(['GET'])
def select(request):
    selects = {
        'tipo': [{'value':'COMPUTADOR','text':'PC / NOTEBOOK'} ,{'value':'IMPRESSORA','text':'IMPRESSORA / SCANNER'}], 
        'marca': [{'value':'DELL','text':'DELL INC.'} ,{'value':'LOGITECH','text':'LOGI'}], 
    }
    
    value = dictModels.get(request.GET.get('metodo')).objects.all().values()
    return Response(value)