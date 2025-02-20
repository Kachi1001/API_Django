from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import psycopg2
from django.conf import settings
from Site_django import util 
from . import models, views, serializers
from PIL import Image
import os

    
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
        }
        sql = funcoes.get(metodo)
    except:
        return funcao_sql(metodo+'()')

    return funcao_sql(sql)

table_models = util.get_classes(models)
table_views = util.get_classes(views)
serial = util.generate_serializer_dicts(serializers)
print(serial)
serial['Select']['indicacao_colaboradores'] = serializers.IndicacaoColaboradores.Select

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tabela_list(request): 
    result = {'tabelas':table_models.keys(),'view':table_views.keys()}
    return Response(result)
serial['Select']
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def select(request, resource):
    return util.create_select(request, resource, serial['Select'])
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tabela(request, table):
    dicts = table_models
    dicts.update(table_views)
    return util.get_table(request, table, dicts, serial['Table'])

resources = util.get_resources(models)
resources['candidato']['select'] += ['indicacao_colaboradores']
@api_view(['GET'])
def resource(request, name):
    if resources.get(name):
        return Response(resources.get(name))
    else:
        return Response({'Error, não encontrado o recurso'}, status=404)

  
from . import views
graficos = {
    # 'ativos_rovatatividade': views.ativos_rotatividade,
    
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
    
class escolaridade_list(util.LC):
    serializer_class = serializers.Escolaridade
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['candidato']


class escolaridade_detail(util.RUD):
    serializer_class = serializers.Escolaridade
    queryset = serializer_class.Meta.model.objects.all()
    
class Anexos_list(util.LC):
    serializer_class = serializers.Anexos
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['candidato']

    @util.database_exception
    def create(self, request, *args, **kwargs):
        import mimetypes

        # Define o caminho base para salvar os arquivos
        base_path = os.path.join(settings.MEDIA_ROOT, 'Curriculos/Anexos')

        # Obtém o arquivo enviado
        file = request.FILES['file']
        file_type = file.content_type  # Obtém o tipo MIME do arquivo
        file_name = request.POST['nome']
        file_ext = '.'

        new_request = request.POST.copy()
        new_request['id'] = request.POST['candidato'] + '_' + request.POST['nome']
        try:
            if file_type.startswith('image/'):  # Caso seja uma imagem
                file_ext = 'jpeg'
                img = Image.open(file).convert('RGB')
                img_path = os.path.join(base_path, f'{new_request['id']}.{file_ext}')
                img.save(img_path, "JPEG", optimize=True, quality=50)

            elif file_type == 'application/pdf':  # Caso seja um PDF
                file_ext = 'pdf'
                pdf_path = os.path.join(base_path, f'{new_request['id']}.{file_ext}')
                with open(pdf_path, 'wb') as pdf_file:
                    for chunk in file.chunks():
                        pdf_file.write(chunk)
                        
            new_request['link'] = f'http://tecnikaengenharia.ddns.net/media/Curriculos/Anexos/{new_request['id']}.{file_ext or 'file'}'
            new_request['tipo'] = file_ext
            
            serializer = self.serializer_class(data=new_request)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
            
        except Exception as e:
            return Response({"error": f"Erro ao processar o arquivo: {str(e)}"}, status=500)
        

class Anexos_detail(util.RUD):
    serializer_class = serializers.Anexos
    queryset = serializer_class.Meta.model.objects.all()
    
    @util.database_exception
    def destroy(self, request, *args, **kwargs):
        try:
            obj = self.serializer_class.Meta.model.objects.get(pk=kwargs['pk'])
            rota = obj.link.replace('http://tecnikaengenharia.ddns.net/media/','')
            os.remove(os.path.join(settings.MEDIA_ROOT, rota))
        except:
            return Response({'error':'Impossível deletar o arquivo'},status=400)
        return super().destroy(request, *args, **kwargs)
    
class experiencia_list(util.LC):
    serializer_class = serializers.Experiencia
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['candidato']

    @util.database_exception
    def list(self, request, *args, **kwargs):
        experiencia_list.serializer_class = serializers.Experiencia.Table
        return super().list(request, *args, **kwargs)

    @util.database_exception
    def create(self, request, *args, **kwargs):
        experiencia_list.serializer_class = serializers.Experiencia
        return super().create(request, *args, **kwargs)
        
class experiencia_detail(util.RUD):
    serializer_class = serializers.Experiencia
    queryset = serializer_class.Meta.model.objects.all()
    
class questionario_list(util.LC):
    serializer_class = serializers.Questionario
    queryset = serializer_class.Meta.model.objects.all()



class questionario_detail(util.RUD):
    serializer_class = serializers.Questionario
    queryset = serializer_class.Meta.model.objects.all()
    
class percepcao_list(util.LC):
    serializer_class = serializers.Percepcao
    queryset = serializer_class.Meta.model.objects.all()


class percepcao_detail(util.RUD):
    serializer_class = serializers.Percepcao
    queryset = serializer_class.Meta.model.objects.all()
    

class entrevista_list(util.LC):
    serializer_class = serializers.Entrevista
    queryset = serializer_class.Meta.model.objects.all()


class entrevista_detail(util.RUD):
    serializer_class = serializers.Entrevista
    queryset = serializer_class.Meta.model.objects.all()

class Profissoes_list(util.LC):
    serializer_class = serializers.Profissoes
    queryset = serializer_class.Meta.model.objects.all().order_by('funcao')


class Profissoes_detail(util.RUD):
    serializer_class = serializers.Profissoes
    queryset = serializer_class.Meta.model.objects.all()
    

        
class Classificacao_list(util.LC):
    serializer_class = serializers.Classificacao
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['candidato']

class Classificacao_detail(util.RUD):
    serializer_class = serializers.Classificacao
    queryset = serializer_class.Meta.model.objects.all()

class AreaAtuacao_list(util.LC):
    serializer_class = serializers.AreaAtuacao
    queryset = serializer_class.Meta.model.objects.all()

class AreaAtuacao_detail(util.RUD):
    serializer_class = serializers.AreaAtuacao
    queryset = serializer_class.Meta.model.objects.all()

class Setor_list(util.LC):
    serializer_class = serializers.Setor
    queryset = serializer_class.Meta.model.objects.all()

class Setor_detail(util.RUD):
    serializer_class = serializers.Setor
    queryset = serializer_class.Meta.model.objects.all()

class AreaAtuacaoSub_list(util.LC):
    serializer_class = serializers.AreaAtuacaoSub
    queryset = serializer_class.Meta.model.objects.all().order_by('sub_area')
    filterset_fields = ['area_atuacao']
class AreaAtuacaoSub_detail(util.RUD):
    serializer_class = serializers.AreaAtuacaoSub
    queryset = serializer_class.Meta.model.objects.all()
    
class Indicacoes_list(util.LC):
    serializer_class = serializers.Indicacoes
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['candidato']
class Indicacoes_detail(util.RUD):
    serializer_class = serializers.Indicacoes
    queryset = serializer_class.Meta.model.objects.all()
    