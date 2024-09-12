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
        print(funcao)
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

@api_view(['POST'])
def register(request):
    parametro = json.loads(request.POST.get('parametro'))
    metodo = request.POST.get('metodo')
    owner = request.POST.get('user')
    if metodo == 'funcao':
        x = objFuncao(Funcao(), parametro)
    elif metodo == 'colaborador':
        x = objColaborador(Colaborador(), parametro)
    elif metodo == 'atividade':
        x = objAtividade(Atividade(), parametro)
    elif metodo == 'supervisor':
        x = objSupervisor(Supervisor(), parametro)
    elif metodo == 'diario':
        if upload(metodo,request.FILES.get('file'),parametro.get('imagem')):
            x = objDiario(Diarioobra(), parametro)
        else: 
            return retorno400
    elif metodo == 'obra':
        try:
            Obra.objects.get(id=parametro.get('id'))
        except ObjectDoesNotExist:
            x = objObra(Obra(), parametro)
        else:
            return Response({'method':'Registro','message':'Houve algum problema, CR já existe'}, status=400)
    elif metodo == 'programacao':
        if upload(metodo,request.FILES.get('file'),parametro.get('imagem')):
            for a in json.loads(parametro.get('lanc')):
                lanc = {
                    'colaborador': a.get('colaborador'),
                    'encarregado': a.get('encarregado'),
                    'obra': a.get('obra'),
                    'iniciosemana': parametro.get('iniciosemana')
                    }
                objProgramacao(Localizacaoprogramada(), lanc)    
            x = True        
        else: 
            return Response({'method':'Registro','message':'Houve algum problema no upload da imagem'}, status=400)
    else:
        return Response({'method':'Registro','message':'Houve algum problema, não encontramos o metodo'}, status=400)
    if x == True:
        return Response({'method':'Registro','message':'Registro efetuado com sucesso!'}, status=200)
    else:
        return x

@api_view(['POST'])
def update(request):
    metodo = request.POST.get('metodo')
    parametro = json.loads(request.POST.get('parametro'))
    owner = request.POST.get('user')
    if metodo == 'colaborador':
        obj = Colaborador.objects.get(id=parametro.get('id'))
        x = objColaborador(obj, parametro) 
    elif metodo == 'obra':
        obj = Obra.objects.get(id=parametro.get('id'))
        x = objObra(obj, parametro)
    elif metodo == 'supervisor':
        obj = Supervisor.objects.get(supervisor=parametro.get('supervisor'))
        x = objSupervisor(obj, parametro)
    elif metodo == 'atividade':
        obj = Atividade.objects.get(id=parametro.get('id'))
        x = objAtividade(obj, parametro)
    elif metodo == 'diario':
        obj = Diarioobra.objects.get(id=parametro.get('id'))
        x = objDiario(obj, parametro)
    elif metodo == 'programacao':
        obj = Localizacaoprogramada.objects.get(id=parametro.get('id'))
        x = objProgramacao(obj, parametro)
    else:
        return Response({'method':'Update','message':'Houve algum problema, não encontramos o metodo'}, status=400)
    if x == True:
        return Response({'method':'Update','message':f'{parametro.get('id')}, foi editado com sucesso'})
    else:
        return x
        
@api_view(['POST'])
def deletar(request):
    metodo = request.POST.get('metodo')
    id = request.POST.get('parametro')
    owner = request.POST.get('user')
    try:
        if metodo == 'colaborador':
            x = Colaborador.objects.get(id=id)
        elif metodo == 'funcao':
            x = Funcao.objects.get(id=id)
        elif metodo == 'supervisor':
            x = Supervisor.objects.get(supervisor=id)
        elif metodo == 'obra':
            x = Obra.objects.get(id=id)
        elif metodo == 'atividade':
            x = Atividade.objects.get(id=id)
        elif metodo == 'diario':
            x = Diarioobra.objects.get(id=id)
        elif metodo == 'programacao':
            x = Localizacaoprogramada.objects.get(id=id)
        else:
            return Response({'method':'Delete','message':'Houve algum problema, não encontramos o metodo'}, status=400)
        x.delete()
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
        elif metodo == 'programacao':
            result = ProgramacaoSerializer(Localizacaoprogramada.objects.get(id=id))
        return Response(result.data,status=200)
    except ObjectDoesNotExist:
            return Response({'method':'Alerta de pesquisa','message': f'id não encontrada <{id}>' }, status=404)

    
