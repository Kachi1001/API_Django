import requests
import time
import threading
from datetime import datetime
import pandas
import os
from Site_django import whatsapp
from .models import * 

def hora():
    return datetime.now().strftime('%d/%m/%Y | %H:%M') + ' -'

horarios = {
    'colaborador': '07:25, 17:55',
    'aprendiz': '13:25, 17:25',
    'estagiario': '07:25,  15:25'
}

def lembrete():
    lembretes = Lembrete.objects.all()
    hora_antiga = '00:00'
    enviado = False
    while run:
        hora = str(datetime.now().strftime('%H:%M'))
        verificado = hora_antiga != hora and datetime.now().weekday() < 5 # se as hora do ultimo teste e do novo ciclo são iguais, e se o dia da semana é menor que 5 (sábado)
        if verificado:
            filtrado = lembretes.filter(padrao='1')
            if len(filtrado) > 0 and not enviado:
                for lembrete in filtrado:
                    valor_coluna1 = lembrete.colaborador
                    valor_coluna2 = lembrete.telefone
                    whatsapp.enviarMSG(
                    numero=     valor_coluna2.replace(' ', '').replace('-', ''),
                    mensagem=   str(f'Olá, *{valor_coluna1.strip()}*\nHora de bater seu ponto digital 🕐📲\nNão se esqueça 😉'), 
                    de=         'dp'
                    )
                    enviado = True
            elif len(filtrado) == 0:
                enviado = False
                
            hora_antiga = hora
        
        if hora == '00:00':
            lembretes = Lembrete.objects.all()

        time.sleep(30)
run = False
console = []
def iniciar(tipo = 'colaborador'):
    global run
    try:
        run = True
        threading.Thread(target=lembrete,args=[['07:25','17:55'], 'colaboradores']).start()
    except:
        run = False
        console.append(f'{hora()} Erro ao iniciar os {tipo}')
    else:
        console.append(f'{hora()} Monitorando os lembretes de {tipo}')
iniciar()

def finalizar(tipo = 'colaborador'):
    run = False