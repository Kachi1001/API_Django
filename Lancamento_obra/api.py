from rest_framework.decorators import api_view
from rest_framework.response import Response
import psycopg2
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import *
import json
from django.http import JsonResponse
from .mani import *
from .serializers import *
from .tables import buildTable
from Home.api import upload

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
        print(funcao)
        cursor.execute(f"SELECT {funcao}")
        conn.commit()
        # Retornando uma resposta de sucesso
        return retorno200
    except psycopg2.Error as e:
        return Response({'error': str(e)}, status=400)
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

@api_view(['POST'])
def register(request):
    parametro = json.loads(request.POST.get('parametro'))
    metodo = request.POST.get('metodo')
    owner = request.POST.get('user') 
    if metodo == 'funcao':
        return objFuncao(Funcao(), parametro)
    elif metodo == 'colaborador':
        return objColaborador(Colaborador(), parametro)
    elif metodo == 'atividade':
        return objAtividade(Atividade(), parametro)
    elif metodo == 'supervisor':
        return objSupervisor(Supervisor(), parametro)
    elif metodo == 'diario':
        if upload('diario',request.FILES.get('file'),parametro.get('imagem')):
            return objDiario(Diarioobra(), parametro)
        else: 
            return retorno400
    elif metodo == 'obra':
        try:
            Obra.objects.get(id=parametro.get('id'))
        except ObjectDoesNotExist:
            return objObra(Obra(), parametro)
        else:
            return Response({'message':'Houve algum problema, CR já existe'}, status=400)
    return Response({'message':'Houve algum problema, não encontramos o metodo'}, status=400)
    

@api_view(['POST'])
def update(request):
    metodo = request.POST.get('metodo')
    parametro = json.loads(request.POST.get('parametro'))
    owner = request.POST.get('user')
    if metodo == 'colaborador':
        obj = Colaborador.objects.get(id=parametro.get('id'))
        return objColaborador(obj, parametro) 
    elif metodo == 'obra':
        obj = Obra.objects.get(id=parametro.get('id'))
        return objObra(obj, parametro)
    elif metodo == 'supervisor':
        obj = Supervisor.objects.get(supervisor=parametro.get('supervisor'))
        return objSupervisor(obj, parametro)
    elif metodo == 'atividade':
        obj = Atividade.objects.get(id=parametro.get('id'))
        return objAtividade(obj, parametro)
    elif metodo == 'diario':
        obj = Diarioobra.objects.get(id=parametro.get('id'))
        return objDiario(obj, parametro)
    else:
        return Response({'message':'Houve algum problema, não encontramos o metodo'}, status=400)

@api_view(['POST'])
def deletar(request):
    metodo = request.POST.get('metodo')
    id = request.POST.get('parametro')
    owner = request.POST.get('user')
    if metodo == 'colaborador':
        return Delete.Colaborador(owner, id) 
    elif metodo == 'funcao':
        return Delete.Funcao(owner, id)
    elif metodo == 'supervisor':
        return Delete.Supervisor(owner, id)
    elif metodo == 'obra':
        return Delete.Obra(owner, id)
    elif metodo == 'atividade':
        return Delete.Atividade(owner, id)
    elif metodo == 'diario':
        return Delete.Diario(owner, id)
    else:
        return Response({'message':'Houve algum problema, não encontramos o metodo'}, status=400)

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
        if parametro == 'atividade':
            value = TipoAtividade.objects.all().values('tipo', 'indice').order_by('indice')
        if parametro == 'obra':
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
        return Response({'message':'Metodo não encontrado'}, status=400)
    else:
        return JsonResponse(list(value), safe=False) 

@api_view(['GET'])
def tabela(request, table):
    return JsonResponse(buildTable(request, table), safe=False)

@api_view(['GET'])
def get_data(request):
    metodo = request.GET.get('metodo')
    id = request.GET.get('parametro')
    result = retorno400
    try:
        if metodo == 'colaborador':
            result = ColaboradorSerializer(Colaborador.objects.get(id=id))
        elif metodo == 'obra':
            result = ObraSerializer(Obra.objects.get(id=id))
        elif metodo == 'atividade':
            result = AtividadeSerializer(Atividade.objects.get(id=id))
        elif metodo == 'diario':
            result = DiarioobraSerializer(Diarioobra.objects.get(diario=id))
        return Response(result.data,status=200)
    except ObjectDoesNotExist:
            return Response({'message': f'Erro de pesquisa: id não encontrada <{id}>'}, status=400)

    
