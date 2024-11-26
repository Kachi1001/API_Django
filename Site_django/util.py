from django.utils import timezone
from rest_framework.response import Response

def formatarDecimal(valor):
    if valor >= 10:
        return str(valor)
    else:
        return '0'+str(valor) 

def formatarHTML(valor):
    return str(valor.year)+ '-' + formatarDecimal(valor.month) + '-' + formatarDecimal(valor.day)

def get_hoje():
    return timezone.now().date()


def create_select(request, resource, Select):

    if resource in Select:
        serial = Select.get(resource)
    else:
        return Response({'method':'Select','message':'Campo não encontrado na API'},status=404)
    
    try:
        queryset = serial.Meta.model.objects.all()    

        values = serial(queryset.order_by('pk'), many= True).data
    except:
        values = serial
    return Response(values)

from rest_framework import generics, status


from django.db import DatabaseError

def database_exception(funcao):
    def wrapper(*args, **kwargs):
        try:
            return funcao(*args, **kwargs)
        except DatabaseError as e:
            return Response(
                {"banco de dados": (str(e).split('CONTEXT')[0])},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    return wrapper
    
class RUD(generics.RetrieveUpdateDestroyAPIView):
    
    @database_exception
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @database_exception
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @database_exception
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @database_exception
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class LC(generics.ListCreateAPIView):
    @database_exception
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @database_exception
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)