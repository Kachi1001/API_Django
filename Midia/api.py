import os
from PIL import Image

from django.conf import settings


caminhos = {
    'carro': 'Reservas/carros/',
    'diario': 'Lancamento_obra/diario/',
    'programacao': 'Lancamento_obra/programacao/'
}
def upload(metodo, file, fileName):
    img = Image.open(file)
    caminho = caminhos.get(metodo)
    path = os.path.join(settings.MIDIA_ROOT, caminho+fileName)

    try:
        img.save(path)
        nome = fileName.split('.')
        os.rename(os.path.join(settings.MIDIA_ROOT, caminho+fileName), os.path.join(settings.MIDIA_ROOT, caminho+nome[0]+'.jpeg'))
    except FileExistsError:
        return True
    else:
        return True 