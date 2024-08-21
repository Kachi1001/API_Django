from django.http import JsonResponse
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q

def getObjects(table):
    if table == 'lancamentos':
        result = Lancamentos.objects.all()
    if table == 'colaborador':
        result = Colaborador.objects.all()
    if table == 'obra':
        result = Obra.objects.all()
    if table == 'diario':
        result = Diarioobra.objects.all()
    return result

def getFilter(table, value):
    if table == 'lancamentos':
        filter = Q(id__icontains=value) | Q(colaborador__icontains=value) | Q(obra__id__icontains=value) | Q(descricao__icontains=value)
    if table == 'colaborador':
        filter = Q(nome__icontains=value) | Q(funcao__icontains=value)
    if table == 'obra':
        filter = Q(empresa__icontains=value)
    if table == 'diario':
        filter = Q(id__icontains=value)
    return filter
        
def buildTable(request, table):
    search_value = request.GET.get('search', '').strip()
    sort_order = request.GET.get('order', 'desc')
    sort_field = request.GET.get('sort', 'id') 
    page_number = int(request.GET.get('offset', 1))
    queryset = getObjects(table)
    
    page_size = int(request.GET.get('limit', 10)) if request.GET.get('limit') else len(queryset)
    # Filtrando com base na busca
    if search_value:
        queryset = queryset.filter(getFilter(table, search_value))  # Ajuste o campo conforme necessário

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