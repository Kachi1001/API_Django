import os
from PIL import Image
from rest_framework.response import Response

from django.conf import settings


caminhos = {
    'carro': 'Reservas/carros/',
    'diario': 'Lancamento_obra/diario/',
    'programacao': 'Lancamento_obra/programacao/'
}
def upload(metodo, file, fileName):
    img = Image.open(file).convert('RGB')
    caminho = caminhos.get(metodo)
    path = os.path.join(settings.MEDIA_ROOT, caminho)

    try:
        nome = fileName.split('.')[0]
        img.save(path + nome + '.jpeg')
    except FileExistsError:
        return Response(status=200)
    except:
        return False
    else:
        return Response(status=200) 