from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
import json
from django.http import JsonResponse
from .mani import mani

dictModels = {
    'maquina': Maquina,
    'padrao': Padrao,
    'produto': Produto,
}

@api_view(['POST'])
def register(request): 
    parametro = json.loads(request.POST.get('parametro'))
    metodo = request.POST.get('metodo')
    owner = request.POST.get('user')
     
    return mani.register(parametro,dictModels.get(metodo)())

    

@api_view(['GET'])
def select(request):
    selects = {
        'tipo': [{'value':'COMPUTADOR','text':'PC / NOTEBOOK'} ,{'value':'IMPRESSORA','text':'IMPRESSORA / SCANNER'}], 
        'marca': [{'value':'DELL','text':'DELL INC.'} ,{'value':'LOGITECH','text':'LOGI'}], 
    }
    value = selects.get(request.GET.get('metodo'))
    return Response(value)

@api_view(['POST'])
def deletar(request):
    return Response({'message':'Houve algum problema, não encontramos o metodo'}, status=400)

@api_view(['GET'])
def get_table(request):
    return Response({'message':'Metodo não encontrado'}, status=400)

@api_view(['GET'])
def get_data(request):
    return Response({'message':'Método não encontrado'}, status=404)

@api_view(['POST'])
def update_supervisor_status(request):
    return Response({'message': f'Erro ao atualizar status:'}, status=400)
    
