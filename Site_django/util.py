from django.utils import timezone
from rest_framework.response import Response
from django.http import JsonResponse

from django.core.cache import cache
from Home.models import AuthUser
from functools import wraps
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
        values = serial
    return Response(values)

from rest_framework import generics


from django.db import DatabaseError

def database_exception(funcao):
    def wrapper(*args, **kwargs):
        action = ''
        request = args[1]
        status = 'Sucesso'
        text = None 
        path = request.META['PATH_INFO'][1:].split('/')
        try:
            action = funcao(*args, **kwargs)
            text = action.data
        except DatabaseError as e:
            status = 'Falhou'
            text = {'data':request.data,'error':str(e)}
            action =  Response(
                {"banco de dados": (str(e).split('CONTEXT')[0])},
                status=500
            )            
        if request.method != 'GET':
            try:
                user = AuthUser.objects.get(id=request.headers.get('X-User-Id'))
                Log.objects.create(user_name=user.username, action=request.method, text=text or path[2] ,app=path[0],resource=path[1],status=status)
            except:
                pass
        return action
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
        return super().list(request, *args, **kwargs)

    @database_exception
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    


def get_table(request, table ,dicts):
    queryset = None
    try:
        queryset = dicts.get(table).objects.all()
    except:
        try:
            queryset = dicts.get(table)
        except:
            return Response({'error':'Tabela não existe no banco ou está desativada'})
    return JsonResponse(buildTable(request, table, queryset))

def buildTable(request, table, queryset):   
    from django.core.paginator import Paginator
    from django.db.models import Q
    fields = request.GET.get('searchable', '').split('%2')[0].split(',')
    search_value = request.GET.get('search', '').strip()
    
    sort_order = request.GET.get('order', 'desc')
    sort_order = 'desc' if sort_order == 'undefined' else sort_order
    sort_field = request.GET.get('sort', 'pk') 
    sort_field = 'pk' if sort_field == 'undefined' else sort_field
    
    page_number = int(request.GET.get('offset', 1))
    # print(json.loads(request.GET.get('filter',))) 
    page_size = int(request.GET.get('limit', 25))
    # Filtrando com base na busca
    if search_value and table:
        preset = Q()
        for x in fields:
            final = x
            if not('_' in x):
                # x = field.split('_')
                # final = x[0] + '__' + x[1] 
                preset |= Q(**{f"{final}__icontains":search_value})
                
            
        queryset = queryset.filter(preset)  # Ajuste o campo conforme necessário

    # Ordenando os dados
    if sort_order == 'asc':
        queryset = queryset.order_by(sort_field)
    else:
        queryset = queryset.order_by(f'-{sort_field}')

    # Paginação
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page_number / page_size + 1)

    data = {
        'total': paginator.count,
        'rows': list(page_obj.object_list.values())  # Ajuste os campos conforme necessário
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
        result[classe.lower()] = getattr(package, classe) 
    return result