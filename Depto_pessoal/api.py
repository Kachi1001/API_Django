from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import psycopg2
from django.conf import settings
from .models import *
from .tables import buildTable
from Site_django import util 
from . import models, views
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
        
@permission_classes([IsAuthenticated]) 
def funcao(request, metodo):
    def format_sql(value):
        value = request.get(value)
        if value != None:
            return "'" + str(value) + "'"
        return 'null'
    def bol_sql(value):
        value = request.get(value)
        if value != None:
            return str(value)
        return 'null'
        
    try:
        funcoes = {
            'muda_cargo': f'muda_cargo({format_sql('id')},{format_sql('data_inicio')},{format_sql('data_fim')},{format_sql('remuneracao')},{format_sql('funcao')},{format_sql('terceiro')},{format_sql('equipe')})',  #nova funcao sql
            'dissidio': f'dissidio({format_sql('id')},{format_sql('data_inicio')},{format_sql('remuneracao')})',
            'desligamento': f'desligamento({format_sql('data')},{format_sql('id')})',
        }
        sql = funcoes.get(metodo)
    except:
        return funcao_sql(metodo+'()')

    return funcao_sql(sql)

from .serializers import *
dictModels = {
    'funcao': Funcao,
    'colaborador': Colaborador,
    'equipe': Equipe,
    'periodoaquisitivo': PeriodoAquisitivo,
    'feriasutilizadas': FeriasUtilizadas,
    'feriasprocessadas': FeriasProcessadas,
    'feriassaldos': views.FeriasSaldos.objects.all(),
    'ocupacao': Ocupacao,
    'ponto': Lembrete,
    'avaliacao': Colaborador.objects.all().filter(avaliacao__isnull=False),
    'feriasmensagem': views.FeriasMensagem.objects.all(),
    'integracao_epi': IntegracaoEpi.objects.all(),
    'integracao_nr': IntegracaoNr.objects.all(),
    'integracao': Integracao.objects.all(),
}

   
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tabela(request, table): 
    # return util.get_table(request, table, dictModels)
    try:
        return Response(buildTable(request, table, dictModels.get(table).objects.all()))
    except:
        return Response(buildTable(request, table, dictModels.get(table)))

from . import models
resources = util.get_resources(models)
resources['colaborador'] = resources['colaborador_']
resources['avaliacao'] = resources['colaborador_']
resources['tipoavaliacao'] = resources['colab_avaliacao']
resources['funcao'] = resources['funcao_']
resources['funcao']['select'].append('categoria')
resources['feriasutilizadas'] = resources['ferias_utilizadas'] 
resources['feriasprocessadas'] = resources['ferias_processadas'] 
resources['periodoaquisitivo'] = resources['periodo_aquisitivo'] 
resources['ponto'] = resources['lembrete'] 
resources['ponto']['select'].append('padrao') 
resources['desligamento'] = {'text':['data', 'id']}
resources['integracao']['select'].append('obra')
@api_view(['GET'])
def resource(request, name):
    return Response(resources.get(name))

  
from . import views
graficos = {
    'rotatividade': views.ativos_rotatividade,
}
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def grafico(request, resource):
    from django.core.exceptions import ObjectDoesNotExist

    try:
        dados = graficos.get(resource).objects.all().values()
        dados = dados[len(dados) -36:]
        return Response(dados,status=200)
    except ObjectDoesNotExist:
        return Response({'method':'Alerta de pesquisa','message': f'id não encontrada <{id}>' }, status=404)

# Colaborador
class colaborador_list(util.LC):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer


class colaborador_detail(util.RUD):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer

    @util.database_exception
    def destroy(self, request, *args, **kwargs):
        return funcao(request.data, 'desligamento')
        # return super().destroy(request, *args, **kwargs)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
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
    serializer_class = OcupacaoSerializer
    queryset = serializer_class.Meta.model.objects.all().order_by('-data_inicio')
    filterset_fields = ['colaborador','id']

class ocupacao_detail(util.RUD):
    serializer_class = OcupacaoSerializer
    queryset = serializer_class.Meta.model.objects.all()
    
    
from django.shortcuts import get_object_or_404
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated]) 
def ocupacao_alterar(request):
    match request.method:
        case 'POST':
            return funcao(request.data, 'muda_cargo')
        case 'GET':
            queryset = Ocupacao.objects.all()
            return Response(OcupacaoSerializer(get_object_or_404(queryset, pk=request.GET['id'])).data)
            
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated]) 
def ocupacao_dissidio(request):
    match request.method:
        case 'POST':
            return funcao(request.data, 'dissidio')
        case 'GET':
            queryset = Ocupacao.objects.all()
            return Response(OcupacaoSerializer(get_object_or_404(queryset, pk=request.GET['id'])).data)
    
#   
# Periodo aquisitivo
class PeriodoAquisitivo_list(util.LC):
    serializer_class = PeriodoAquisitivoSerializer
    queryset = serializer_class.Meta.model.objects.all().order_by('-adquirido_em')
    filterset_fields = ['colaborador']
    
    
class PeriodoAquisitivo_detail(util.RUD):
    serializer_class = PeriodoAquisitivoSerializer
    queryset = serializer_class.Meta.model.objects.all()
    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def PeriodoAquisitivo_funcao(request):
    return funcao(request, 'periodo_aquisitivo')

    
#   
# Ferias processadas
class FeriasProcessadas_list(util.LC):
    serializer_class = FeriasProcessadasSerializer
    queryset = FeriasProcessadas.objects.all().order_by('-id')
    
    filterset_fields = ['colaborador']

            
class FeriasProcessadas_detail(util.RUD):
    queryset = FeriasProcessadas.objects.all()
    serializer_class = FeriasProcessadasSerializer

# 
# Ferias utilizadas
class FeriasUtilizadas_list(util.LC):
    serializer_class = FeriasUtilizadasSerializer
    queryset = FeriasUtilizadas.objects.all().order_by('-id')
    
    filterset_fields = ['colaborador']
            
class FeriasUtilizadas_detail(util.RUD):
    queryset = FeriasUtilizadas.objects.all()
    serializer_class = FeriasUtilizadasSerializer
    

# Lembrete
from rest_framework.permissions import IsAuthenticatedOrReadOnly
class Lembrete_list(util.LC):
    permission_classes = [IsAuthenticatedOrReadOnly]
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
    
class Avaliacao():
    serializer_class = AvaliacaoSerializer
    queryset = serializer_class.Meta.model.objects.all().filter(avaliacao__isnull=False)

class Avaliacao_list(Avaliacao,util.LC):
    pass

class Avaliacao_detail(Avaliacao,util.RUD):
    pass
    
class TipoAvaliacao():
    serializer_class = TipoAvaliacaoSerializer
    queryset = serializer_class.Meta.model.objects.all()

class TipoAvaliacao_list(TipoAvaliacao,util.LC):
    pass
    
class TipoAvaliacao_detail(TipoAvaliacao,util.RUD):
    pass
    
        
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def select(request, resource):
    from .serializers import Select

    return util.create_select(request, resource, Select)
        
from django.core.cache import cache
        
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated]) 
def app_menu(request, app):
    base = f'Depto_pessoal:app:{app}:'
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
    try: feriados = Feriado.objects.get(id=util.get_hoje())
    except Feriado.DoesNotExist: return Response(0)
    else: return Response(1)

class IntegracaoNr_list(util.LC):
    serializer_class = IntegracaoNrSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['colaborador','id']

class IntegracaoNr_detail(util.RUD):
    serializer_class = IntegracaoNrSerializer    
    queryset = serializer_class.Meta.model.objects.all()
    
class Integracao_list(util.LC):
    serializer_class = IntegracaoSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['colaborador','id']

class Integracao_detail(util.RUD):
    serializer_class = IntegracaoSerializer    
    queryset = serializer_class.Meta.model.objects.all()
    
class IntegracaoEpi_list(util.LC):
    serializer_class = IntegracaoEpiSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['colaborador','id']

class IntegracaoEpi_detail(util.RUD):
    serializer_class = IntegracaoEpiSerializer    
    queryset = serializer_class.Meta.model.objects.all()
    
# Feriado
class Lembrete(util.LC):
    serializer_class = LembreteSerial
    queryset = serializer_class.Meta.model.objects.all()
        