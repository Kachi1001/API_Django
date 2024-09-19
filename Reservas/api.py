from Reservas.serializers import *
from Reservas.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from media.api import upload
from Site_Django import whatsapp
retorno200 = Response({'message':'Sucesso'}, status=200)
retorno400 = Response({'message':'Método não encontrado'}, status=400)
retorno404 = Response({'message':'Registro não encontrado'}, status=404)
    
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
    elif metodo == 'atendimento' or metodo == 'apoio' or metodo == 'reuniao':
        return Response(reservaSala(request))
    else:
        return retorno400
        
@api_view(['POST'])
def delete(request):
    metodo = request.POST.get('metodo')
    parametro = json.loads(request.POST.get('parametro'))
    if metodo == "sala":
        try:    
            x = AgendaSalas.objects.get(id=parametro.get('id'))
            x.delete()
            return retorno200
        except AgendaSalas.DoesNotExist:
            return retorno404
    else:
        return retorno400
    
@api_view(['POST'])
def edit(request):
    metodo = request.POST.get('metodo')
    parametro = request.POST.get('parametro')
    if metodo == 'sala':
        try:
            x = AgendaSalas.objects.get(id=parametro.get('id'))
            x.responsavel = parametro.get('responsavel')
            x.descricao = parametro.get('descricao')
            x.save()
            return retorno200
        except AgendaSalas.DoesNotExist:
            return retorno404
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
            return Response({'message':'Esses seguintes horários já estão reservados '+str(conflito)},status=406)
        else:
            msg = []
            resp = None
            for a in horas:
                if resp == None:
                    resp = a.get('responsavel')

                z = AgendaSalas(hora=a.get('hora'), data=parametro.get('data'), responsavel=a.get('responsavel'), sala=parametro.get('sala'), descricao=a.get('descricao'),reservado='checked disabled')
                z.save()

                if resp != a.get('responsavel'):
                    whatsapp.enviarMSG('5535126392',{'sala': z.sala, 'resp': resp, 'data':z.data, 'horas':msg})
                    resp = a.get('responsavel')
                    msg = []
                msg.append(z.hora)
                
            whatsapp.enviarMSG('5535126392',{'sala': z.sala, 'resp': resp, 'data':z.data, 'horas':msg})
            return retorno200
    else:
        return retorno400

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
        a = AgendaSalas(hora=horario, responsavel='', reservado='',descricao='') #cria um vazio
        try:
            a = reservados.get(hora=horario)
        except:
            return Response({'message':'teste'})
        else:
            resultado.append(a)
    return(resultado)

from Site_Django import util
def reservaSala(request):
    horarios1= ["07:30","08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30"]
    horarios2= ["13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30"]
    metodo = request.GET.get('metodo')
    parametro = json.loads(request.POST.get('parametro'))
    date = parametro.data if parametro.data != None else util.formatarHTML(util.get_hoje())
    reservados = AgendaSalas.objects.all().filter(sala=metodo, data=date)
    
    if metodo == 'atendimento':
        if parametro.horario == 'manha':
            return gerarLista(reservados, horarios1)
        elif parametro.horario == 'tarde':
            return gerarLista(reservados, horarios2)
         
        