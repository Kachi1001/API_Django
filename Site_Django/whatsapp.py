import requests
url = 'http://10.0.0.139:3000/client/sendMessage/felipe'
def enviarMSG(numero,mensagem):
    obj = {"chatId": f"55{numero}@c.us","contentType": "string","content": str(mensagem)}
    headers = {'accept': '*/*', 'Content-Type': 'application/json', 'x-api-key':'comunidadezdg.com.br'}
    requests.post(url, json=obj, headers=headers)
    return