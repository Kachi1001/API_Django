from django.core.paginator import Paginator
from django.db.models import Q


def buildTable(request, table, queryset):
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