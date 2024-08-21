from .models import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json

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
                    conflito.append(y.hora + '-' + y.responsavel + '-' + y.descricao)
        
        if len(conflito) > 0:
            return Response({'message':'Esses seguintes horários já estão reservados '+str(conflito)},status=406)
        else:
            for a in horas:
                z = AgendaSalas(hora=a, data=parametro.get('data'), responsavel=parametro.get('responsavel'), sala=parametro.get('sala'), descricao=parametro.get('descricao'),reservado='checked disabled')
                z.save()
            return Response({'message':'Sucesso'})
        
    elif metodo == 'reservar_simples':
        horas = json.loads(parametro.get('reservas'))
        
        conflito = []
        reservas = AgendaSalas.objects.all().filter(data=parametro.get('data'), sala=parametro.get('sala'))
        for x in horas:
            for y in reservas:
                if x.get('hora') == y.hora:
                    conflito.append(y.hora + '-' + y.responsavel + '-' + y.descricao)
                    
        if len(conflito) > 0:
            return Response({'message':'Esses seguintes horários já estão reservados '+str(conflito)},status=406)
        else:
            for a in horas:
                z = AgendaSalas(hora=a.get('hora'), data=parametro.get('data'), responsavel=a.get('responsavel'), sala=parametro.get('sala'), descricao=a.get('descricao'),reservado='checked disabled')
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

def getCarro(request):
    try:
        mymodel = Carros.objects.get(placa=request.GET.get('id'))
        serializer = CarrosSerializer(mymodel)
        return Response(serializer.data)
    except Carros.DoesNotExist:
        return Response(status=400)
