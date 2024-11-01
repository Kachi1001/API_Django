from .models import *
from .views import *
from django.core.paginator import Paginator
from django.db.models import Q
value = None
def buildTable(request, table, queryset):
    search_value = request.GET.get('search', '').strip()
    filtros = {
        'atividade':Q(id__icontains=search_value) | Q(colaborador__icontains=search_value) | Q(obra__id__icontains=search_value) | Q(diario__icontains=search_value),
        'colaborador':Q(nome__icontains=search_value) | Q(funcao__icontains=search_value),
        'obra':Q(empresa__icontains=search_value) | Q(id__icontains=search_value) | Q(cidade__icontains=search_value),
        'diario':Q(id__icontains=search_value) | Q(data__icontains=search_value) | Q(obra__id__icontains=search_value) | Q(encarregado__icontains=search_value),
        'incompletos':Q(nome__icontains=search_value) | Q(dia__icontains=search_value) | Q(obra__icontains=search_value) | Q(encarregado__icontains=search_value),
        'hora_mes':Q(colaborador__icontains=search_value) | Q(competencia__icontains=search_value) | Q(contrato__icontains=search_value),
        'programacao':Q(colaborador__icontains=search_value) | Q(obra__id__icontains=search_value) | Q(iniciosemana__icontains=search_value) | Q(encarregado__icontains=search_value),
        'descontos_resumo':Q(encarregado__icontains=search_value) | Q(colaborador__icontains=search_value) | Q(dia__icontains=search_value),
        'diarias':Q(competencia__icontains=search_value) | Q(colaborador__icontains=search_value),
        'alocacoes':Q(colaborador__icontains=search_value) | Q(obra__icontains=search_value),
    }
    
    sort_order = request.GET.get('order', 'desc')
    sort_field = request.GET.get('sort', 'pk') 
    page_number = int(request.GET.get('offset', 1))
    # print(json.loads(request.GET.get('filter',))) 
    page_size = int(request.GET.get('limit', 10)) if request.GET.get('limit') else len(queryset)
    # Filtrando com base na busca
    if search_value and table in filtros:
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