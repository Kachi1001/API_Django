import requests
from decouple import config

url = 'http://10.0.0.139:3000/client/sendMessage/'
def enviarMSG(numero,mensagem,de):
    obj = {"chatId": f"55{numero}@c.us","contentType": "string","content": str(mensagem)}
    headers = {'accept': '*/*', 'Content-Type': 'application/json', 'x-api-key':config('WP_API', 'tecnika.com.br')}
    requests.post(url+de, json=obj, headers=headers)
    return