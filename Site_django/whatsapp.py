from decouple import config
import threading
import requests

url = 'http://10.0.0.139:3000/client/sendMessage/'
api_key = config('WP_KEY')
def enviarMSG(numero, mensagem, de):
    def funcao():
        url = 'http://10.0.0.139:3000/client/sendMessage/'
        obj = {"chatId": f"55{numero}@c.us", "contentType": "string", "content": str(mensagem)}
        headers = {'accept': '*/*', 'Content-Type': 'application/json', 'x-api-key': api_key}
        requests.post(url + de, json=obj, headers=headers)

    x = threading.Thread(target=funcao)
    x.start()
    x = None