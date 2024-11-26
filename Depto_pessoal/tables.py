from .models import *
from .serializers import *
from django.core.paginator import Paginator
from django.db.models import Q

def buildTable(request, table, queryset):
    search_value = request.GET.get('search', '').strip()
    filtros = {
        'colaborador':Q(nome__icontains=search_value) | Q(id__icontains=search_value) | Q(equipe__icontains=search_value),
        'ferias_processadas':Q(colaborador__nome__icontains=search_value) | Q(dias_processados__icontains=search_value) | Q(data_inicio__icontains=search_value) | Q(periodo_aquisitivo__id__icontains=search_value),
        'ferias_utilizadas':Q(colaborador__nome__icontains=search_value) | Q(dias_utilizados__icontains=search_value) | Q(data_inicio__icontains=search_value) | Q(periodo_aquisitivo__id__icontains=search_value),
        'periodo_aquisitivo':Q(colaborador__nome__icontains=search_value) | Q(adquirido_em__icontains=search_value) | Q(periodo__icontains=search_value) | Q(id__icontains=search_value),
        'lembrete':Q(colaborador__icontains=search_value)
    }
    serializadores= {
        'ferias_processadas': FeriasProcessadasTable,
        'ferias_utilizadas': FeriasUtilizadasTable,
        'periodo_aquisitivo': PeriodoAquisitivoTable,
        'avaliacao': AvaliacaoTable,
    }
    sort_order = request.GET.get('order', 'desc')
    sort_field = request.GET.get('sort', 'pk') 
    page_number = int(request.GET.get('offset', 1))
    # print(json.loads(request.GET.get('filter',))) 
    page_size = int(request.GET.get('limit', 10)) if request.GET.get('limit') else len(queryset)
    # Filtrando com base na busca
    if search_value:
        queryset = queryset.filter(filtros.get(table, ''))  # Ajuste o campo conforme necessário

    # Ordenando os dados
    if sort_order == 'asc':
        queryset = queryset.order_by(sort_field)
    else:
        queryset = queryset.order_by(f'-{sort_field}')

    # Paginação
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page_number / page_size + 1)

    if table in serializadores:
        rows = serializadores.get(table)(page_obj.object_list, many=True).data
    else:
        rows = list(page_obj.object_list.values())
    
    data = {
        'total': paginator.count,
        'rows': rows  # Ajuste os campos conforme necessário
    }
    return data