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

    try:
        funcoes = {
            'muda_cargo': f'muda_cargo({format_sql('id')},{format_sql('data_inicio')},{format_sql('data_fim')},{format_sql('remuneracao')},{format_sql('funcao')})',
            'dissidio': f'dissidio({format_sql('id')},{format_sql('data_inicio')},{format_sql('remuneracao')})',
            'desligamento': f'desligamento({format_sql('data')},{format_sql('id')})',
        }
        sql = funcoes.get(metodo)
    except:
        return funcao_sql(metodo+'()')

    return funcao_sql(sql)

from . import models, views, serializers
table_models = util.get_classes(models)
table_views = util.get_classes(views)
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tabela(request, table):
    dicts = table_models
    dicts.update(table_views)
    return util.get_table(request, table, dicts)

resources = util.get_resources(models)
@api_view(['GET'])
def resource(request, name):
    return Response(resources.get(name))

  
from . import views
graficos = {
    'ativos_rovatatividade': views.ativos_rotatividade,
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
class candidato_list(util.LC):
    serializer_class = serializers.Candidato
    queryset = serializer_class.Meta.model.objects.all()


class candidato_detail(util.RUD):
    serializer_class = serializers.Candidato
    queryset = serializer_class.Meta.model.objects.all()
    

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def select(request, resource):
    from .serializers import Select

    return util.create_select(request, resource, Select)
        
