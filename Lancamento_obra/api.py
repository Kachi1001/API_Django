import os
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
from Site_django import media, tables, util

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
        e = str(e).split('\n')[0]
        return Response({'error': e}, status=400)
    else:
        return Response({'method':'Atualizar','message':'Tabela atualizada com sucesso'}, status=200)

    finally:
        cursor.close()
        conn.close()
        

@api_view(['POST'])
def funcao(request, funcao):
    def get_formatter(value, padrao= None):
        value = parametro.get(value, padrao)
        if value != None:
            return "'" + str(value) + "'"
        return 'null'
        
    funcao_void = ['atualizar_tabelas',]
    if funcao in funcao_void:
        return funçãoSQL(funcao+'()')
    parametro = request.data
    if funcao == 'efetividade':
        return funçãoSQL(f"get_efetividade({get_formatter('colaborador')},{get_formatter('obra')},{get_formatter("dataini")},{get_formatter("datafim")})")
    elif funcao == 'subconsulta_lancamento':
        return funçãoSQL(f"{funcao}('{parametro.get("colaborador", '')}','{parametro.get("dia", '2050-01-01')}')")
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
    'descontos_resumo': DescontosResumo,
    'diarias':Diarias,
    'efetividade':Efetividade,
    'hora_mes':HoraMes,
    'incompletos':Incompletos,
    'fechados': Tecnicon,
    'alocacoes': Alocacoes,
}

@api_view(['POST'])
def register(request):
    parametro = json.loads(request.POST.get('parametro'))
    metodo = request.POST.get('metodo')
    obj = dictModels.get(metodo)
    owner = request.POST.get('user')
    
    if metodo == 'diario':
        if media.upload(metodo,request.FILES.get('file'),parametro.get('imagem')).status_code:
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
        if media.upload(metodo,request.FILES.get('file'),parametro.get('imagem')):
            for a in json.loads(parametro.get('lanc')):
                a['iniciosemana'] = parametro.get('iniciosemana')
                x=mani.create(a,obj())
                if x.status_code != 200: 
                    return x
            return Response({'method':'Sucesso','message':'Cadastro efetuado com sucesso!'}, status=200)
        else: 
            return Response({'method':'Registro','message':'Houve algum problema no upload da imagem'}, status=400)
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
    metodos = {
        'select': {
            'funcao': Funcao.objects.all().values('funcao'),
            'supervisor_id': Supervisor.objects.all().filter(ativo=True).values('supervisor', 'ativo').order_by('supervisor'),
            'obra_id': Obra.objects.all().order_by('id').values('id', 'empresa', 'cidade', 'finalizada'),
            'atividade_id': TipoAtividade.objects.all().values('tipo', 'indice').order_by('indice'), 
            'colaborador': Colaborador.objects.all().values('id', 'nome', 'demissao').order_by('nome'),
            'encarregado': Colaborador.objects.all().filter(encarregado=True).values('id', 'nome').order_by('nome')
        },
        'table': {
            'funcao': Funcao.objects.all().values('funcao', 'id'),
            'supervisor': Supervisor.objects.all().values('supervisor', 'ativo')
        }
    }
    value = metodos.get(metodo).get(parametro)
    if value == None:
        return Response({'method':'Tabela','message':'Método não encontrado'}, status=400)
    else:
        return JsonResponse(list(value), safe=False) 

@api_view(['GET'])
def tabela(request, table):
    return JsonResponse(tables.buildTable(request, table, dictModels.get(table).objects.all()), safe=False)

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
    
from openpyxl import load_workbook
from django.http import HttpResponse
@api_view(['GET'])
def diario_impressao(request):
    obra = Obra.objects.get(id=request.GET['cr'])

    colabs = Localizacaoprogramada.objects.all().filter(obra=request.GET['cr'],iniciosemana=request.GET['data'])
        
    arquivo = load_workbook(os.path.join(settings.BASE_DIR, 'template/xlsx/diario.xlsx'))
    aba = arquivo['CONTROLE']
    aba['W2'] = obra.empresa
    aba['W4'] = obra.cidade
    aba['D7'] = obra.descricao
    aba['I9'] = obra.id
    aba['O9'] = obra.orcamento
    # aba['B57'] = obra.etapas or ' '

    tick = 0
    while tick <= 25:
        try:
            aba[f'C{tick + 22}'] = colabs[tick].colaborador
            tick += 1
        except:
            break
            
    # Criar a resposta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=diário.xlsx'

    # Salvar o arquivo no HttpResponse
    arquivo.save(response)

    return response

@api_view(['GET'])
def select(request, resource):
    from .serializers import Select

    return util.create_select(request, resource, Select)


@api_view(['GET'])
def resource(request, name):
    resources = {
        'atividade': {
            'text': [
                "id",
                "dia",
                "descricao",
                "indice",
                "horaini1",
                "horafim1",
                "horaini2",
                "horafim2",
                "horaini3",
                "horafim3",
                "motivo",
                'etapa1',
                'etapa2',
                'etapa3',
            ],
            'check': ["diaseguinte", "meiadiaria"],
            'select': [
                "obra",
                "atividade",
                "colaborador",
                "supervisor",
            ],
        },
        'colaborador': { 
            'text': [
                "id",
                "nome",
                "admissao",
                "contrato",
                "diaria",
                "observacao",
                "demissao",
            ],
            "check": ["encarregado"],
            "select": ["funcao"]
        },
        'obra': {
            'text': [
                "id",
                "orcamento",
                "empresa",
                "cidade",
                "descricao",
                "retrabalho",
                "tecnicon",
            ],
            "check": ["finalizada"],
            'select': ["indice","supervisor"]
        },
        'diario': {
            'text': [
                "id",
                "diario",
                "indice",
                "data",
                "climamanha",
                "climatarde",
                "descricao",
            ],
            'select': ["encarregado", "obra"],
            'check': []
        },
        'supervisor': {
            'text': ['id'], 'check':['ativo']},
        'funcao': {
            'text':['funcao', 'grupo']},
        'programacao': {
            'text': ['id','observacao', 'iniciosemana'], 
            'select': ['colaborador', 'encarregado','obra'],
            'check': []},
    }
    
    return Response(resources.get(name))


from rest_framework import generics, status
class Colaborador_list(util.LC):
    serializer_class = ColaboradorSerializer
    queryset = ColaboradorSerializer.Meta.model.objects.all().order_by('nome')
    filterset_fields = {
        'demissao': ['isnull'],  # Permite filtrar por isnull e valores exatos
        'nome': ['exact', 'icontains'],       # Exemplo de filtro para nome
        'encarregado': ['exact'],       # Exemplo de filtro para nome
    }

    
class Colaborador_detail(util.RUD):
    serializer_class = ColaboradorSerializer
    queryset = ColaboradorSerializer.Meta.model.objects.all()
    
    
class Obra_list(util.LC):
    serializer_class = ObraSerializer
    queryset = serializer_class.Meta.model.objects.all().order_by('id')
    filterset_fields = ['finalizada']


class Obra_detail(util.RUD):
    serializer_class = ObraSerializer
    queryset = serializer_class.Meta.model.objects.all()
    
class Funcao():
    serializer_class = FuncaoSerializer
    queryset = serializer_class.Meta.model.objects.all()

class Funcao_list(Funcao, util.LC):
    pass

class Funcao_detail(Funcao, util.RUD):
    pass

class Supervisor():
    serializer_class = SupervisorSerializer
    queryset = serializer_class.Meta.model.objects.all()

class Supervisor_list(Supervisor, util.LC):
    pass

class Supervisor_detail(Supervisor, util.RUD):
    pass    
    
class Atividade_list(util.LC):
    serializer_class = AtividadeSerializer
    queryset = serializer_class.Meta.model.objects.all().order_by('id')


class Atividade_detail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AtividadeSerializer
    queryset = serializer_class.Meta.model.objects.all()

class Diarioobra_list(util.LC):
    serializer_class = DiarioobraSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['diario']
    
    @util.database_exception
    def create(self, request, *args, **kwargs):
        parametro = json.loads(request.POST.get('parametro'))
        
        if media.upload('diario',request.FILES.get('file'),parametro.get('imagem')).status_code:
            diario = DiarioobraSerializer(data=parametro)
            if diario.is_valid():
                diario.save()
                return Response(diario.data,status=status.HTTP_201_CREATED) 
            else:
                media.delete('diario', parametro.get('imagem'))
                return Response(diario.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
        else: 
            return Response(request,status=status.HTTP_406_NOT_ACCEPTABLE)
            
    
class Diarioobra_detail(util.RUD):
    serializer_class = DiarioobraSerializer
    queryset = serializer_class.Meta.model.objects.all()
    

class Programacao_list(util.LC):
    serializer_class = ProgramacaoSerializer
    queryset = serializer_class.Meta.model.objects.all()

    @util.database_exception
    def create(self, request, *args, **kwargs):
        parametro = json.loads(request.POST.get('parametro'))

        if media.upload('programacao',request.FILES.get('file'),parametro.get('imagem')).status_code:
            for a in json.loads(parametro.get('lanc')):
                a['iniciosemana'] = parametro.get('iniciosemana')
                a['id'] = 'qualquer'
                
                programacao = ProgramacaoSerializer(data=a)
                if programacao.is_valid():
                    programacao.save()
                else:
                    media.delete('programacao', parametro.get('imagem'))
                    return Response(programacao.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'sucesso'},status=status.HTTP_201_CREATED) 
        else: 
            return Response(request,status=status.HTTP_406_NOT_ACCEPTABLE)
        
class Programacao_detail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProgramacaoSerializer
    queryset = serializer_class.Meta.model.objects.all()
