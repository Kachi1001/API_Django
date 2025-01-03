from .models import *
from .serializers import *
from django.core.paginator import Paginator
from django.db.models import Q

def buildTable(request, table, queryset):
    search_value = request.GET.get('search', '').strip()
    filtros = {
        'colaborador':Q(nome__icontains=search_value) | Q(id__icontains=search_value) | Q(equipe__icontains=search_value),
        'feriasprocessadas':Q(id__icontains=search_value) | Q(colaborador__nome__icontains=search_value) | Q(dias_processados__icontains=search_value) | Q(data_inicio__icontains=search_value) | Q(periodo_aquisitivo__id__icontains=search_value),
        'feriasutilizadas':Q(id__icontains=search_value) | Q(colaborador__nome__icontains=search_value) | Q(dias_utilizados__icontains=search_value) | Q(data_inicio__icontains=search_value) | Q(periodo_aquisitivo__id__icontains=search_value),
        'periodoaquisitivo':Q(id__icontains=search_value) | Q(colaborador__nome__icontains=search_value) | Q(adquirido_em__icontains=search_value) | Q(periodo__icontains=search_value) | Q(id__icontains=search_value),
        'ponto':Q(colaborador__icontains=search_value),
        'feriassaldos':Q(colaborador__icontains=search_value),
        'avaliacao':Q(nome__icontains=search_value) | Q(avaliacao__id__icontains=search_value) | Q(cpf__icontains=search_value) | Q(rg__icontains=search_value),
        'integracao_nr': Q(colaborador__nome__icontains=search_value) | Q(nr__id__icontains=search_value) ,
        'integracao_epi': Q(colaborador__nome__icontains=search_value),
        'integracao': Q(colaborador__nome__icontains=search_value),
    }
    serializadores= {
        'feriasprocessadas': FeriasProcessadasTable,
        'feriasutilizadas': FeriasUtilizadasTable,
        'periodoaquisitivo': PeriodoAquisitivoTable,
        'avaliacao': AvaliacaoTable,
        'integracao_nr': IntegracaoNrSerializer.Table,
        'integracao_epi': IntegracaoEpiSerializer.Table,
        'integracao': IntegracaoSerializer.Table,
    }
    sort_order = request.GET.get('order', 'desc')
    sort_order = 'desc' if sort_order == 'undefined' else sort_order
    sort_field = request.GET.get('sort', 'pk') 
    sort_field = 'pk' if sort_field == 'undefined' else sort_field
    
    page_number = int(request.GET.get('offset', 1))
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