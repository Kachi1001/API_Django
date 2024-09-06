from django.http import JsonResponse
from .models import *
from .views import *
from django.core.paginator import Paginator
from django.db.models import Q

def getTable(tabela, value):
    if tabela == 'atividade':
        retorno = {
            'data': Atividade.objects.all(),
            'filter': Q(id__icontains=value) | Q(colaborador__icontains=value) | Q(obra__id__icontains=value) | Q(diario__icontains=value)
        }
    elif tabela == 'colaborador':
        retorno = {
            'data':Colaborador.objects.all(),
            'filter':Q(nome__icontains=value) | Q(funcao__icontains=value)            
        }
    elif tabela == 'obra':
        retorno = {
        'data':Obra.objects.all(),
        'filter' :Q(empresa__icontains=value) | Q(id__icontains=value) | Q(cidade__icontains=value)
        }
    elif tabela == 'diario':
        retorno = {
        'data':Diarioobra.objects.all(),
        'filter':Q(id__icontains=value)
        }
    elif tabela == 'incompletos':
        retorno = {
        'data':Incompletos.objects.all(),
        'filter':Q(nome__icontains=value) | Q(dia__icontains=value) | Q(obra__icontains=value) | Q(encarregado__icontains=value)
        }
        
    elif tabela == 'hora_mes':
        retorno = {
        'data':HoraMes.objects.all(),
        'filter':Q(colaborador__icontains=value) | Q(competencia__icontains=value)
        }
    elif tabela == 'efetividade':
        retorno = {
        'data':Efetividade.objects.all(),
        'filter':''
        }
    return retorno

    
def buildTable(request, table):
    search_value = request.GET.get('search', '').strip()
    values = getTable(table, search_value)
    sort_order = request.GET.get('order', 'desc')
    sort_field = request.GET.get('sort', 'pk') 
    page_number = int(request.GET.get('offset', 1))
    queryset = values['data']
    # print(json.loads(request.GET.get('filter',))) 
    page_size = int(request.GET.get('limit', 10)) if request.GET.get('limit') else len(queryset)
    # Filtrando com base na busca
    if search_value:
        queryset = queryset.filter(values['filter'])  # Ajuste o campo conforme necessário

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