from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from Site_django import whatsapp
import random
from django.core.cache import cache
import asyncio

retorno200 = Response({'message':'Sucesso'}, status=200)
retorno400 = Response({'message':'Método não encontrado'}, status=400)
retorno404 = Response({'message':'Registro não encontrado'}, status=404)
    

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




from rest_framework import generics

class agendasala_list(generics.ListCreateAPIView):
    serializer_class = AgendaSalasSerializer
    queryset = AgendaSalas.objects.all()
    filterset_fields = ['sala','data','hora']
    
    def create(self, request):
        data = request.data['reservas']
        
        # Verificar se é possivel reservar
        conflito = []
        queryset = AgendaSalas.objects.all().filter(data=data[0].get('data'), sala=data[0].get('sala'))
        for reserva in data:
            filtered = queryset.filter(hora=reserva.get('hora')).exists()

            if filtered:
                conflito.append(reserva['hora'] + '-' + reserva['responsavel'])


        # Reservar senão possuir conflito   
        if len(conflito) > 0:
            return Response({'Conflitos':'Esses seguintes horários já estão reservados '+str(conflito)},status=406)
        
        msg = []
        resp = None
        for a in data:
            if resp == None:
                resp = a.get('responsavel')
                
            z = AgendaSalas(hora=a.get('hora'), data=a.get('data'), responsavel=a.get('responsavel'), sala=a.get('sala'), descricao=a.get('descricao'),reservado='checked disabled')
            z.save()
            
            if resp != a.get('responsavel'):
                whatsapp.enviarMSG('5584543627',mensagem,'gestao-dados')
                
                resp = a.get('responsavel')
                msg = []
                
            msg.append(z.hora)
            mensagem = f'*Sala Reservada*\nSala: _{z.sala}_\nData: _{datetime.strptime(z.data, '%Y-%m-%d').strftime('%d/%m/%Y')}_\nResponsável: _{resp.strip()}_\nhttp://tecnikaengenharia.ddns.net/Reservas/sala/{z.sala}?data={z.data}'
            
        whatsapp.enviarMSG('5584543627',mensagem,'gestao-dados')
        cache.set('Reservas:lastick:sala',random.randint(1,100))
        
        return Response({'method':'Reserva de sala', 'message':'Reservas realizadas com sucesso!'})


class agendasala_detail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AgendaSalasSerializer
    queryset = AgendaSalas.objects.all()
    
    
@api_view(['GET'])
def agendasala_quadro(request):
            horarios_dict = {
                'manha': ["07:30","08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30"],
                'tarde': ["13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30"]
            }
            # metodo = request.GET.get('metodo')
            parametro = request.GET
            date = parametro.get('data', util.formatarHTML(util.get_hoje()))
            reservados = AgendaSalas.objects.all().filter(sala=parametro.get('sala','atendimento'), data=date).values('hora','responsavel','reservado','descricao')

            return Response({'dados':gerarLista(reservados, horarios_dict.get(parametro.get('horario','manha'))), 'method':'Carregar dados','message':'Sucesso em ler'}) 
            

@api_view(['GET'])
def lastick(request, resource):
    result = cache.get(f'Reservas:{resource}:lastick')
        
    if not result:
        result = random.randint(1,100)
        cache.set('Reservas:lastick:sala',result)
            
    return Response(data=result)