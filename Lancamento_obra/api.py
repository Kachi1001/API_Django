from rest_framework.decorators import api_view
from rest_framework.response import Response
import psycopg2
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .views import *
import json
from django.http import JsonResponse
from .mani import *
from .serializers import *
from .tables import buildTable
from media.api import upload

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
    funcao_void = ['atualizar_tabelas']
    metodo = request.GET.get('metodo')
    if metodo in funcao_void:
        return funçãoSQL(metodo+'()')

    parametro = json.loads(request.GET.get('parametro'))
    if metodo == 'efetividade':
        return funçãoSQL(f"get_efetividade('{parametro.get("colaborador", '')}','{parametro.get("obra" , '')}','{parametro.get("dataini", '2000-01-01')}','{parametro.get("datafim", '2050-01-01')}')")
    
    return retorno400



dictModels = {
    'funcao': Funcao,
    'diario': Diarioobra,
    'obra': Obra,
    'programacao': Localizacaoprogramada,
    'atividade': Atividade,
    'supervisor': Supervisor,
    'funcao': Funcao,
    'colaborador': Colaborador,
}

@api_view(['POST'])
def register(request):
    parametro = json.loads(request.POST.get('parametro'))
    metodo = request.POST.get('metodo')
    obj = dictModels.get(metodo)()
    owner = request.POST.get('user')
    
    if metodo == 'diario':
        if upload(metodo,request.FILES.get('file'),parametro.get('imagem')):
            pass
        else: 
            return retorno400
    elif metodo == 'obra':
        try:
            obj.objects.get(id=parametro.get('id'))
        except ObjectDoesNotExist:
            pass
        else:
            return Response({'method':'Registro','message':'Houve algum problema, CR já existe'}, status=400)
    elif metodo == 'programacao':
        if upload(metodo,request.FILES.get('file'),parametro.get('imagem')):
            for a in json.loads(parametro.get('lanc')):
                a['iniciosemana'] = parametro.get('iniciosemana')
                mani.create(a,obj)
            return retorno200
        else: 
            return Response({'method':'Registro','message':'Houve algum problema no upload da imagem'}, status=400)
    return mani.create(parametro,obj)
    
@api_view(['POST'])
def update(request):
    metodo = request.POST.get('metodo')
    parametro = json.loads(request.POST.get('parametro'))
    owner = request.POST.get('user')
    if metodo == 'supervisor':
        obj = Supervisor.objects.get(supervisor=parametro.get('supervisor'))
    else:
        obj = dictModels.get(metodo).objects.get(id=parametro.get('id'))
    return mani.update(parametro,obj)
          
    
    
        
@api_view(['POST'])
def deletar(request):
    metodo = request.POST.get('metodo')
    id = request.POST.get('parametro')
    owner = request.POST.get('user')
    try:
        if metodo == 'supervisor':
            obj = Supervisor.objects.get(supervisor=id)
        else:
            obj = dictModels.get(metodo).objects.get(id=id)
        obj.delete()
    except ObjectDoesNotExist as e:
        return Response({'method': 'Delete','message':'Item não encontrado'}, status=400)
    except DatabaseError as e:
        return Response({'method':'Delete','message': str(e)}, status=400)
    else:
        return Response({'method':'Delete','message':f'{id}, foi deletado com sucesso'})
        
@api_view(['GET'])
def get_table(request):
    metodo = request.GET.get('metodo')
    parametro = request.GET.get('parametro')
    value = None
    if metodo == 'select':
        if parametro == 'funcao':
            value = Funcao.objects.all().values('funcao')
        if parametro == 'supervisor':
            value = Supervisor.objects.all().filter(ativo=True).values('supervisor', 'ativo').order_by('supervisor')
        if parametro == 'atividade_id':
            value = TipoAtividade.objects.all().values('tipo', 'indice').order_by('indice')
        if parametro == 'obra_id':
            value = Obra.objects.all().order_by('id').values('id', 'empresa', 'cidade', 'finalizada')
        if parametro == 'colaborador':
            value = Colaborador.objects.all().values('id', 'nome', 'demissao').order_by('nome')
        if parametro == 'encarregado':
            value = Colaborador.objects.all().filter(encarregado=True).values('id', 'nome').order_by('nome')
    elif metodo == 'table':
        if parametro == 'funcao':
            value = Funcao.objects.all().values('funcao', 'id')
        if parametro == 'supervisor':
            value = Supervisor.objects.all().values('supervisor', 'ativo')
    if value == None:
        return Response({'method':'Tabela','message':'Método não encontrado'}, status=400)
    else:
        return JsonResponse(list(value), safe=False) 

@api_view(['GET'])
def tabela(request, table):
    return JsonResponse(buildTable(request, table), safe=False)

@api_view(['GET'])
def get_data(request):
    metodo = request.GET.get('metodo')
    id = request.GET.get('parametro')
    obj = dictModels.get(metodo).objects.all().filter(id=id)
    result = retorno400
    try:
        value = obj.values()
        return JsonResponse(list(value), safe=False) 
    except ObjectDoesNotExist:
            return Response({'method':'Alerta de pesquisa','message': f'id não encontrada <{id}>' }, status=404)

@api_view(['GET'])
def grafico(request):
    metodo = request.GET.get('metodo')
    result = retorno400
    try:
        if metodo == 'grafico1':
            return Response(Graficos.objects.all().values('mes','hora_50','hora_100'),status=200)
    except ObjectDoesNotExist:
            return Response({'method':'Alerta de pesquisa','message': f'id não encontrada <{id}>' }, status=404)
    
