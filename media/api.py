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
    elif metodo == 'programacao':
        caminho = 'lancamento_obra/programacao/'
    if caminho == None:
        return False
    else:
        path = os.path.join(settings.MEDIA_ROOT, caminho+fileName)
        img.save(path) 
        nome = fileName.split('.')
        os.rename(os.path.join(settings.MEDIA_ROOT, caminho+fileName), os.path.join(settings.MEDIA_ROOT, caminho+nome[0]+'.jpeg'))
        return True