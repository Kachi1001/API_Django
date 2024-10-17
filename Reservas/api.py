from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from Media.api import upload
from Site_django import whatsapp
from datetime import datetime
retorno200 = Response({'message':'Sucesso'}, status=200)
retorno400 = Response({'message':'Método não encontrado'}, status=400)
retorno404 = Response({'message':'Registro não encontrado'}, status=404)
latestTick = {
    'reservasala':datetime.now()
}
@api_view(['GET'])
def get(request):
    metodo = request.GET.get('metodo')
    parametro = request.GET.get('parametro')
    if metodo == 'carro':
        try:
            serializer = CarrosSerializer(Carros.objects.get(placa=parametro))
            return Response(serializer.data)
        except Carros.DoesNotExist:
            return retorno404
    elif metodo in ['atendimento','apoio', 'reunião', 'auxiliar']:
        return reservaSala(request)
    elif metodo == 'latestTick':
        return Response(data=latestTick.get(parametro))
    else:
        return Response({'message':'Método não encontrado','method':'Requisição'}, status=400)
        
@api_view(['DELETE'])
def delete(request):
    metodo = request.POST.get('metodo')
    parametro = json.loads(request.POST.get('parametro'))
    if metodo == "sala":
        try:    
            x = AgendaSalas.objects.get(id=parametro.get('id'))
            x.delete()

        except AgendaSalas.DoesNotExist:
            return Response({'method':'Delete','message':'Reserva não existe mais'}, status=400)
        else:
            return Response({'method':'Delete','message':'Concluído a exclusão com exito'}, status=200)
            
    else:
        return retorno400
    
@api_view(['PATCH'])
def edit(request):
    metodo = request.POST.get('metodo')
    parametro = json.loads(request.POST.get('parametro'))
    if metodo == 'sala':
        try:
            x = AgendaSalas.objects.get(id=parametro.get('id'))
            x.responsavel = parametro.get('responsavel')
            x.descricao = parametro.get('descricao')
            x.save()
        except AgendaSalas.DoesNotExist:
            return retorno404
        else:
            return Response({'method':'Edição','message':'Concluído a exclusão com exito'}, status=200)
            
    else:
        return retorno400


@api_view(['POST'])
def register(request):
    metodo = request.POST.get('metodo')
    parametro = json.loads(request.POST.get('parametro'))
    if metodo == 'carro':
        if parametro.get('placa'):
            if upload('carro',request.FILES.get('file'),parametro.get('imagem')):
                c = Carros.objects.create(placa=parametro.get('placa'), modelo=parametro.get('modelo'),marca=parametro.get('marca'),imagem=parametro.get('imagem'))
                return retorno200
            else:
                return retorno400
        else:
            return Response({'message': f'Erro ao adicionar carro: Placa não pode ser nulo'}, status=400)
    elif metodo == 'reservar_sala':
        horas = json.loads(parametro.get('reservas'))
        
        conflito = []
        reservas = AgendaSalas.objects.all().filter(data=parametro.get('data'), sala=parametro.get('sala'))
        for x in horas:
            for y in reservas:
                if x.get('hora') == y.hora:
                    conflito.append(y.hora + '-' + y.responsavel + '-' + y.descricao)
                    
        if len(conflito) > 0:
            return Response({'method':'Conflitos','message':'Esses seguintes horários já estão reservados '+str(conflito)},status=406)
        else:
            msg = []
            resp = None
            for a in horas:
                if resp == None:
                    resp = a.get('responsavel')

                z = AgendaSalas(hora=a.get('hora'), data=parametro.get('data'), responsavel=a.get('responsavel'), sala=parametro.get('sala'), descricao=a.get('descricao'),reservado='checked disabled')
                z.save()
                
                if resp != a.get('responsavel'):
                    whatsapp.enviarMSG('5535126392',mensagem)
                    resp = a.get('responsavel')
                    msg = []
                msg.append(z.hora)
                mensagem = f'*Sala Reservada*\nSala: _{z.sala}_\nData: _{z.data}_\nResponsável: _{resp}_\nHorários: _{msg}_'
                
            whatsapp.enviarMSG('5535126392',mensagem)
            global latestTick 
            latestTick["reservasala"] = datetime.now()
            return Response({'method':'Reserva de sala', 'message':'Reservas realizadas com sucesso!'})
    else:
        return Response({'method':'Erro desconhecido', 'message':'Método não encontrado'})

def gerarListaCarros(reservados, listaCarros):
    resultado = []
    for carro in listaCarros:
        a = AgendaCarros(carro=carro,reservado='Disponível',responsavel="",destino="")
        b = reservados.filter(carro=carro)
        for c in b:
            a = AgendaCarros(carro=carro,data=c.data,responsavel=c.responsavel,destino=c.destino,reservado=c.reservado)
        resultado.append(a)
    return(resultado)

def gerarLista(reservados, horarios):
    resultado = []
    for horario in horarios:
        try:
            a = reservados.filter(hora=horario)[0]
        except:
            a = {'hora':horario, 'responsavel':'', 'reservado':'','descricao':''}#cria um vazio
        finally:
            resultado.append(a)
    return resultado

from Site_django import util
def reservaSala(request):
    horarios_dict = {
        'manha': ["07:30","08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30"],
        'tarde': ["13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30"]
    }
    metodo = request.GET.get('metodo')
    parametro = json.loads(request.GET.get('parametro'))
    date = parametro.get('data') if parametro.get('data') != None else util.formatarHTML(util.get_hoje())
    reservados = AgendaSalas.objects.all().filter(sala=metodo, data=date).values('hora','responsavel','reservado','descricao')

    return Response({'dados':gerarLista(reservados, horarios_dict.get(parametro.get('horario'))), 'method':'Carregar dados','message':'Sucesso em ler'}) 

         
        