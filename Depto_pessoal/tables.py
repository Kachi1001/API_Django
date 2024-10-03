from .models import *
from django.core.paginator import Paginator
from django.db.models import Q

def buildTable(request, table, queryset):
    search_value = request.GET.get('search', '').strip()
    filtros = {
        'colaborador':Q(nome__icontains=search_value) | Q(funcao__icontains=search_value),
    }
    
    sort_order = request.GET.get('order', 'desc')
    sort_field = request.GET.get('sort', 'pk') 
    page_number = int(request.GET.get('offset', 1))
    # print(json.loads(request.GET.get('filter',))) 
    page_size = int(request.GET.get('limit', 10)) if request.GET.get('limit') else len(queryset)
    # Filtrando com base na busca
    if search_value:
        queryset = queryset.filter(filtros.get(table))  # Ajuste o campo conforme necessário

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