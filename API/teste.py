# myapp/views.py
from django.http import JsonResponse
from django.core.paginator import Paginator
from models.Lancamento_obra.models import *


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def server_side_data(request):
    draw = request.GET.get('draw')
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    order_column = request.GET.get('order[0][column]')
    order = request.GET.get(f'columns[{order_column}][data]')
    order_dir = request.GET.get('order[0][dir]')
    search_value = request.GET.get('search[value]', '')

    # Ordenação
    if order_dir == 'desc':
        order = '-' + order

    queryset = Lancamentos.objects.all()

    # Filtragem
    if search_value:
        queryset = queryset.filter(name__icontains=search_value)

    # Paginação
    paginator = Paginator(queryset.order_by(order), length)
    page = paginator.get_page(start // length + 1)

    data = []
    for obj in page:
        data.append({
            'id': obj.id,
            'colaborador': obj.colaborador,
            'obra': obj.obra.cr,
        })

    response = {
        'draw': draw,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
        'data': data,
    }

    return JsonResponse(response)
