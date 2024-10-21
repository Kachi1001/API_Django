import requests
import time
import threading
from datetime import datetime
import pandas
import os
from Site_django import whatsapp
from . import models 


# Cria o caminho completo para o arquivo

def enviarMSG(colaborador, numero):
    headers = {'accept': '*/*', 'Content-Type': 'application/json', 'x-api-key':'tecnika.com.br'}
    url = 'http://10.0.0.139:3000/client/sendMessage/dp'
    obj = {
        "chatId": f"55{numero}@c.us",
        "contentType": "string",
        "content": str(f'Olá, *{colaborador}*\nHora de bater seu ponto digital 🕐📲\nNão se esqueça 😉')
        }
    requests.post(url, json=obj, headers=headers)

def lembrete(horas, planilha):
    caminho_arquivo = os.path.join(diretorio_planilhas, planilha+'.xlsx')
    bd = pandas.read_excel(caminho_arquivo)
    print(f'Esperando os horários: {horas}, e evitando os finais de semana [{planilha}]')
    hora_antiga = '00:00'
    enviado = False
    while True:
        hora = str(datetime.now().strftime('%H:%M'))
        verificado = hora_antiga != hora and datetime.now().weekday() < 5 # se as hora do ultimo teste e do novo ciclo são iguais, e se o dia da semana é menor que 5 (sábado)
        if verificado:
            hora_antiga = hora
            if hora_antiga in horas and not enviado:
                for index, row in bd.iterrows():
                    valor_coluna1 = str(row['NOME'])
                    valor_coluna2 = str(row['CONTATO'])
                    enviarMSG(valor_coluna1.strip(), valor_coluna2.replace(' ', '').replace('-', ''))
                enviado = True
                print(f"{datetime.now().strftime('%d/%m/%Y | %H:%M')} - enviando mensagem para os {planilha}")
            elif not (hora_antiga in horas):
                enviado = False
        time.sleep(10)
        
        if hora == '00:00':
            bd = pandas.read_excel(caminho_arquivo)
            
Tcolab_run = False
Tcolab = threading.Thread(target=lembrete,args=[['07:25','17:55'], 'colaboradores'])

def iniciar():
    Tcolab.start()

def finalizar():
    Tcolab.online = False