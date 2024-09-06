import os
from PIL import Image

from django.conf import settings



def upload(metodo, file, fileName):
    img = Image.open(file)
    caminho = None
    if metodo == 'carro':
        caminho = 'reservas/carros/'
    elif metodo == 'diario':
        caminho = 'lancamento_obra/diarios/'
    if caminho == None:
        return False
    else:
        path = os.path.join(settings.MEDIA_ROOT, caminho+fileName)
        img.save(path) 
        return True