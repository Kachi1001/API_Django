from django.utils import timezone
from rest_framework.response import Response
from django.http import JsonResponse

from django.core.cache import cache
from Home.models import AuthUser
from functools import wraps

from django.conf import settings
import psycopg2
def funcao_sql(request, sql): 
    app = request.META['PATH_INFO'][1:].split('/')[0]
    db = settings.DATABASES['default']
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
        return Response({'Atualizar':'Executado com sucesso com sucesso'}, status=200)

    finally:
        cursor.close()
        conn.close()

def format_sql(request, value):
    value = request.get(value)
    if value != None:
        return "'" + str(value) + "'"
    return 'null'

def cached(ttl=60):  # TTL (tempo de vida) em segundos
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            chave = f"{func.__name__}:{args}:{kwargs}"
            resultado = cache.get(chave )
            if resultado:
                return resultado
            resultado = func(*args, **kwargs)
            cache.set(chave, resultado, ttl)
            return resultado
        return wrapper
    return decorator

def formatarDecimal(valor):
    if valor >= 10:
        return str(valor)
    else:
        return '0'+str(valor) 

def formatarHTML(valor):
    return str(valor.year)+ '-' + formatarDecimal(valor.month) + '-' + formatarDecimal(valor.day)

def get_hoje():
    return timezone.now().date()

def get_agora():
    return timezone.now()


def create_select(request, resource, Select):

    if resource in Select:
        serial = Select.get(resource)
    else:
        return Response({'method':'Select','message':'Campo não encontrado na API'},status=404)
    
    try:
        queryset = serial.Meta.model.objects.all()
        values = serial(queryset.order_by('pk'), many= True).data
    except:
        try:
            values = serial()
        except :
            values = serial
    return Response(values)

from rest_framework import generics


from django.db import DatabaseError

def get_user(request):
    return AuthUser.objects.get(id=request.headers.get('X-User-Id'))


def database_exception(funcao):
    def wrapper(*args, **kwargs):
        try:
            return funcao(*args, **kwargs)
        except DatabaseError as e:
            return Response(
                {"banco de dados": (str(e).split('CONTEXT')[0])},
                status=500
            )            
        
    return wrapper

from Home.models import Log
from rest_framework.permissions import IsAuthenticated  
class RUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )    
    
    @database_exception
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @database_exception
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # @database_exception
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)

    @database_exception
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class LC(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    
    @database_exception
    def list(self, request, *args, **kwargs):
        try: self.serializer_class = self.serializer_class.Table
        except: pass
        return super().list(request, *args, **kwargs)

    @database_exception
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    


def get_table(request, table ,dicts, serializers = {}):
    serializer = serializers.get(table)
    try:
        return JsonResponse(buildTable(request, dicts.get(table).objects.all(), serializer))
    except Exception as e:
        print(e)
        try:
            return JsonResponse(buildTable(request, dicts.get(table), serializer))
        except Exception as e:
            return Response({'error':f'Tabela não existe no banco ou está desativada {e}'},404)

def buildTable(request, queryset, serializer):   
    from django.core.paginator import Paginator
    from django.db.models import Q
    fields = request.GET.get('searchable', '').split('%2')[0].split(',')
    search_value = request.GET.get('search', '').strip()
    
    sort_order = request.GET.get('order', 'desc')
    sort_order = 'desc' if sort_order == 'undefined' else sort_order
    sort_field = request.GET.get('sort', 'pk') 
    sort_field = 'pk' if sort_field == 'undefined' else sort_field
    
    page_number = int(request.GET.get('offset', 1))

    page_size = int(request.GET.get('limit', 25))
    # Filtrando com base na busca
    if search_value:
        preset = Q()
        for x in fields:
            final = x
            if not('_' in x):
                # x = field.split('_')
                # final = x[0] + '__' + x[1] 
                preset |= Q(**{f"{final}__icontains":search_value})
                
        try:
            queryset = queryset.filter(preset)  # Ajuste o campo conforme necessário
        except Exception as e:
            print(e)

    # Ordenando os dados
    if sort_order == 'asc':
        queryset = queryset.order_by(sort_field)
    else:
        queryset = queryset.order_by(f'-{sort_field}')

    # Paginação
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page_number / page_size + 1)

    rows = serializer(page_obj.object_list, many=True).data if serializer else list(page_obj.object_list.values())

    data = {
        'total': paginator.count,
        'rows': rows  # Ajuste os campos conforme necessário
    }
    return data

def get_resources(models):
    classes = [nome for nome in dir(models) if nome.startswith('') and callable(getattr(models, nome))]
    resources = {}
    for resource in classes:
        classe = resource
        resource = {'text':[], 'select':[], 'check':[]}
        for field, valor in vars(getattr(models, classe)).items():
            if not any(x in field for x in ['_set', 'get_', '__', '_meta','DoesNotExist','MultipleObjectsReturned','objects','_id']):
                tipo = str(vars(valor).items()).split('<')[1].split(':')[0].split('.') 
                if tipo[len(tipo) - 1] == 'BooleanField':
                    resource['check'].append(field)
                else:
                    for detail, name in vars(valor).items():
                        for x in vars(name).items():
                            if x[0] == 'db_column':
                                if x[1] != None:
                                    resource['select'].append(field)
                                else:
                                    resource['text'].append(field)
            elif field == '_meta':
                for key, value in vars(valor).items():
                    if key == 'db_table':
                        resource_name = value
        resources[resource_name] = resource
    return resources

def get_classes(package):
    result = {}
    classes = [nome for nome in dir(package) if nome.startswith('') and callable(getattr(package, nome))]
    for classe in classes:
        for field, valor in vars(getattr(package, classe)).items():
            if field == '_meta':
                for key, value in vars(valor).items():
                    if key == 'db_table':
                        result[value] = getattr(package, classe) 
    return result