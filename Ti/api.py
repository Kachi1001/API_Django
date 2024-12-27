from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
    
from django.core.cache import cache

@api_view(['POST','GET'])
def app(request):
    base = 'Ti:app:'
    status = 200
    if request.method == 'POST':
        ca = cache.get(f'{base}toggle')
        ca = not bool(ca)
        cache.set(f'{base}toggle', int(ca), None)
        status = 202
    values = cache.get_many([f'{base}run',f'{base}toggle'])
    return Response(values,status=status)
        