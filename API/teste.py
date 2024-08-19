# myapp/views.py
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Lancamentos
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def server_side_data(request):
    draw = request.GET.get('draw')
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    order_column = request.GET.get('order[0][column]') or 0
    order = request.GET.get(f'columns[{order_column}][data]') 
    order_dir = request.GET.get('order[0][dir]')
    search_value = request.GET.get('search[value]', '')

    # Ordenação
    if order_dir == 'desc':
        order = '-' + order

    queryset = Lancamentos.objects.all()

    # Filtragem
    if search_value:
        queryset = queryset.filter(
            Q(id__icontains=search_value) |
            Q(colaborador__icontains=search_value) |  # supondo que 'nome' seja o campo relevante em colaborador
            Q(obra__cr__icontains=search_value)  # supondo que 'nome' seja o campo relevante em obra
        )
    # Paginação
    paginator = Paginator(queryset.order_by(order), length)
    page = paginator.get_page(start // length + 1)

    data = []
    for obj in page:
        data.append({
            'id': obj.id,
            'colaborador': obj.colaborador,
            'dia': obj.dia,
            'descricao': obj.descricao,
            'horaini1': obj.horaini1,
            'horafim1': obj.horafim1,
            'horaini2': obj.horaini2,
            'horafim2': obj.horafim2,
            'horaini3': obj.horaini3,
            'horafim3': obj.horafim3,
            'atividade': obj.atividade.tipo,
            'diario': obj.diario,
            'obra': obj.obra.cr,
        })

    response = {
        'draw': draw,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
        'data': data,
    }

    return JsonResponse(response)
