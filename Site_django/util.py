from django.utils import timezone
from rest_framework.response import Response

def formatarDecimal(valor):
    if valor >= 10:
        return str(valor)
    else:
        return '0'+str(valor) 

def formatarHTML(valor):
    return str(valor.year)+ '-' + formatarDecimal(valor.month) + '-' + formatarDecimal(valor.day)

def get_hoje():
    return timezone.now().date()


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

from rest_framework import generics, status


from django.db import DatabaseError

def database_exception(funcao):
    def wrapper(*args, **kwargs):
        try:
            return funcao(*args, **kwargs)
        except DatabaseError as e:
            return Response(
                {"banco de dados": (str(e).split('CONTEXT')[0])},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    return wrapper
    
class RUD(generics.RetrieveUpdateDestroyAPIView):
    
    @database_exception
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @database_exception
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @database_exception
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @database_exception
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class LC(generics.ListCreateAPIView):
    @database_exception
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @database_exception
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    


def buildTable(request, table, queryset):
    from django.core.paginator import Paginator
    from django.db.models import Q
    fields = dict(request.GET).get('searchable[]')
    search_value = request.GET.get('search', '').strip()
    
    sort_order = request.GET.get('order', 'desc')
    sort_field = request.GET.get('sort', 'pk') 
    page_number = int(request.GET.get('offset', 1))
    # print(json.loads(request.GET.get('filter',))) 
    page_size = int(request.GET.get('limit', len(queryset)))
    # Filtrando com base na busca
    if search_value and table:
        preset = Q()
        for field in fields:
            final = field
            if not('_' in field):
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