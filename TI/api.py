from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
import json
from django.http import JsonResponse
from .mani import *
from .serializers import *

from .tables import buildTable

@api_view(['POST'])
def cadastrar(request): 
    parametro = json.loads(request.POST.get('parametro'))
    metodo = request.POST.get('metodo')
    owner = request.POST.get('user') 
    if metodo == 'computador':
        return Register.Funcao(owner, parametro)
    elif metodo == 'colaborador':
        return Register.Colaborador(owner, parametro)
    elif metodo == 'Historico':
        return Register.Historico("1",'teste','create','teste')
    elif metodo == 'supervisor':
        return Register.Supervisor(owner, parametro)
    elif metodo == "Carro":
        return Register.Carro(owner, parametro)
    return Response({'message':'Houve algum problema, não encontramos o metodo'}, status=400)
    

@api_view(['POST'])
def update(request):
    metodo = request.POST.get('metodo')
    parametro = json.loads(request.POST.get('parametro'))
    owner = request.POST.get('user')
    if metodo == 'colaborador':
        return Edit.Colaborador(owner, parametro) 
    elif metodo == 'obra':
        return Edit.Obra(owner, parametro)
    elif metodo == 'lancamento':
        return Edit.Lancamentos(owner, parametro)
    return Response({'message':'Houve algum problema, não encontramos o metodo'}, status=400)

@api_view(['POST'])
def deletar(request):
    metodo = request.POST.get('metodo')
    id = request.POST.get('parametro')
    owner = request.POST.get('user')
    if metodo == 'colaborador':
        return Delete.Colaborador(owner, id) 
    elif metodo == 'funcao':
        return Delete.Funcao(owner, id)
    elif metodo == 'supervisor':
        return Delete.Supervisor(owner, id)
    elif metodo == 'obra':
        return Delete.Obra(owner, id)
    elif metodo == 'lancamento':
        return Delete.Lancamentos(owner, id)
    return Response({'message':'Houve algum problema, não encontramos o metodo'}, status=400)

@api_view(['GET'])
def get_table(request):
    metodo = request.GET.get('metodo')
    parametro = request.GET.get('parametro')
    value = None
    if metodo == 'select':
        if parametro == 'selectFuncao':
            value = Funcao.objects.all().values('funcao')
        if parametro == 'selectSupervisor':
            value = Supervisor.objects.all().values('supervisor', 'ativo')
        if parametro == 'selectAtividade':
            value = Atividade.objects.all().values('tipo')
        if parametro == 'selectObra':
            value = Obra.objects.all().values('id', 'empresa', 'cidade')
        if parametro == 'selectColaborador':
            value = Colaborador.objects.all().values('id', 'nome')
    elif metodo == 'table':
        if parametro == 'funcao':
            value = Funcao.objects.all().values('funcao')
        if parametro == 'supervisor':
            value = Supervisor.objects.all().values('supervisor', 'ativo')
    if value == None:
        return Response({'message':'Metodo não encontrado'}, status=400)
    else:
        return JsonResponse(list(value), safe=False) 

@api_view(['GET'])
def tabela(request, table):
    return JsonResponse(buildTable(request, table), safe=False)

@api_view(['GET'])
def get_data(request):
    metodo = request.GET.get('metodo')
    id = request.GET.get('parametro')
    if metodo == 'colaborador':
        try:
            mymodel = Colaborador.objects.get(id=id)
            serializer = ColaboradorSerializer(mymodel)
            return Response(serializer.data)
        except Colaborador.DoesNotExist:
            return Response({'message':'Colaborador não existe'}, status=400)
    elif metodo == 'obra':
        try:
            mymodel = Obra.objects.get(id=id)
            serializer = ObraSerializer(mymodel)
            return Response(serializer.data)
        except Obra.DoesNotExist:
            return Response({'message':'Obra não encontrada'}, status=400)
    elif metodo == 'lancamento':
        try:
            mymodel = Lancamentos.objects.get(id=id)
            serializer = LancamentosSerializer(mymodel)
            return Response(serializer.data)
        except Lancamentos.DoesNotExist:
            return Response({'message':'Lançamento não encontrada'},status=400)
    else:
        return Response({'message':'Método não encontrado'}, status=404)

@api_view(['POST'])
def update_supervisor_status(request):
    name = request.POST.get('supervisor')
    ativo = True if request.POST.get('ativo') == 'true' else False
    try: 
        supervisor = Supervisor.objects.get(supervisor=name)
        supervisor.ativo = ativo
        supervisor.save()
        return Response({'message': 'Status atualizado com sucesso'})
    except Supervisor.DoesNotExist:
        return Response({'message': 'Supervisor não encontrado'}, status=404)
    except Exception as e:
        return Response({'message': f'Erro ao atualizar status: {str(e)}'}, status=400)
    
