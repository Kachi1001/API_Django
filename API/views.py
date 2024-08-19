from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import psycopg2
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json   
from django.http import JsonResponse
from .mani import *
from .serializers import *
from PIL import Image
import os
from pathlib import Path 

# Configurações de conexão com o banco de dados PostgreSQL
dbname = settings.DATABASES['default']['NAME']
user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
host = settings.DATABASES['default']['HOST']
port = settings.DATABASES['default']['PORT']

@api_view(['POST'])
def executar_funcao_geraViewJunta(request): 
    # Parâmetro passado pelo front end
    parametro = request.GET.get('parametro')

    # Conectando ao banco de dados
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    
    try:
        # Executando a função
        cursor.execute("SELECT gera_view_junta()")
        conn.commit()

        # Retornando uma resposta de sucesso
        return Response({'message': 'Tabela criada com sucesso'})

    except psycopg2.Error as e:
        return Response({'error': str(e)}, status=400)

    finally:
        cursor.close()
        conn.close()

@api_view(['POST'])
def cadastrar(request):
    parametro = json.loads(request.POST.get('parametro'))
    metodo = request.POST.get('metodo')
    owner = request.POST.get('user') 
    if metodo == 'Funcao':
        return Register.Funcao(owner, parametro)
    elif metodo == 'Colaborador':
        return Register.Colaborador(owner, parametro)
    elif metodo == 'Historico':
        return Register.Historico("1",'teste','create','teste')
    elif metodo == 'Supervisor':
        return Register.Supervisor(owner, parametro)
    elif metodo == "Carro":
        return Register.Carro(owner, parametro)

@api_view(['POST'])
def update(request):
    metodo = request.POST.get('metodo')
    parametro = json.loads(request.POST.get('parametro'))
    owner = request.POST.get('user')
    if metodo == 'Colaborador':
        return Edit.Colaborador(owner, parametro) 
    elif metodo == 'Obra':
        return Edit.Obra(owner, parametro)
    elif metodo == 'Lancamentos':
        return Edit.Lancamentos(owner, parametro)
    return Response({'message':'Houve algum problema, não encontramos o metodo'}, status=400)

@api_view(['POST'])
def deletar(request):
    metodo = request.POST.get('metodo')
    id = request.POST.get('parametro')
    owner = request.POST.get('user')
    if metodo == 'Colaborador':
        return Delete.Colaborador(owner, id) 
    elif metodo == 'Funcao':
        return Delete.Funcao(owner, id)
    elif metodo == 'Supervisor':
        return Delete.Supervisor(owner, id)
    elif metodo == 'Obra':
        return Delete.Obra(owner, id)
    elif metodo == 'Lancamentos':
        return Delete.Lancamentos(owner, id)
    
@api_view(['POST'])
def salas(request):
    metodo = request.POST.get('metodo')
    parametro = json.loads(request.POST.get('parametro'))
    if metodo == 'reservar_multi':
        if parametro.get('responsavel') == '' or parametro.get('data') == '':
            return Response({'message':'Precisa informar uma data e um responsável para reservar a sala'},status=400)
        horas = json.loads(parametro.get('horarios'))
        conflito = []
        reservas = AgendaSalas.objects.all().filter(data=parametro.get('data'), sala=parametro.get('sala'))
        for x in horas:
            for y in reservas:
                if x == y.hora:
                    conflito.append(x)
        if len(conflito) > 0:
            return Response({'message':'Esses seguintes horários ja estão reservados '+str(conflito)},status=406)
        else:
            for a in horas:
                z = AgendaSalas(hora=a, data=parametro.get('data'), responsavel=parametro.get('responsavel'), sala=parametro.get('sala'), descricao=parametro.get('descricao'),reservado='checked disabled')
                z.save()
            return Response({'message':'Sucesso'})
    else:
        x = AgendaSalas.objects.get(id=parametro.get('id'))
        if metodo == "deletar":
            x.delete()
            return Response({'message':'Deletado com sucesso'})
        elif metodo == 'editar':
            x.responsavel = parametro.get('responsavel')
            x.descricao = parametro.get('descricao')
            x.save()
            return Response({'message':'Editado com sucesso'})
        else:
            return Response({'message':'Houve algum problema'})
                

@api_view(['GET'])
def get_table(request):
    table = request.GET.get('tableDB')
    if table == 'funcao':
        value = Funcao.objects.all().values('funcao', 'grupo')
    elif table == 'supervisor':
        value = Supervisor.objects.all().values('supervisor', 'ativo')
    elif table == 'atividade':
        value = Atividade.objects.all().values('tipo')
    elif table == 'obra':
        value = Obra.objects.all().values('cr', 'empresa', 'cidade')
    elif table == 'colaborador':
        value = Colaborador.objects.all().values('id', 'nome')
    return JsonResponse(list(value), safe=False)

@api_view(['GET'])
def get_data(request):
    metodo = request.GET.get('metodo')
    id = request.GET.get('id')
    if metodo == 'colab':
        try:
            mymodel = Colaborador.objects.get(id=id)
            serializer = ColaboradorSerializer(mymodel)
            return Response(serializer.data)
        except Colaborador.DoesNotExist:
            return Response({'message':'teste'}, status=400)
    elif metodo == 'Obra':
        try:
            mymodel = Obra.objects.get(cr=request.GET.get('id'))
            serializer = ObraSerializer(mymodel)
            return Response(serializer.data)
        except Obra.DoesNotExist:
            return Response(status=400)
    elif metodo == 'Lancamentos':
        try:
            mymodel = Lancamentos.objects.get(id=request.GET.get('id'))
            serializer = LancamentosSerializer(mymodel)
            return Response(serializer.data)
        except Lancamentos.DoesNotExist:
            return Response(status=400)
    elif metodo == 'Carro':
        try:
            mymodel = Carros.objects.get(placa=request.GET.get('id'))
            serializer = CarrosSerializer(mymodel)
            return Response(serializer.data)
        except Carros.DoesNotExist:
            return Response(status=400)
            
    else:
        return Response({'message':'Houve algum problema'}, status=404)

@api_view(['POST'])
def update_supervisor_status(request):
    try:
        supervisor_name = request.POST.get('supervisor')
        ativo = request.POST.get('ativo') == 'true'
        supervisor = Supervisor.objects.get(supervisor=supervisor_name, ativo=ativo)
        supervisor.save()
        return Response({'message': 'Status atualizado com sucesso'})
    except Supervisor.DoesNotExist:
        return Response({'message': 'Supervisor não encontrado'}, status=404)
    except Exception as e:
        return Response({'message': f'Erro ao atualizar status: {str(e)}'}, status=400)
    
@api_view(['POST'])
def upload_file(request):
    if request.FILES.get('file'):
        img = Image.open(request.FILES.get('file'))
        path = os.path.join(settings.MEDIA_ROOT, f'reservas/carros/{request.POST.get('placa')}.jpg')
        img = img.save(path) 
        return JsonResponse({'message': 'Upload com sucesso'}, status=200)
    return JsonResponse({'error': 'Nenhum arquivo enviado'}, status=400)
    