import os
from PIL import Image
from pathlib import Path 
from django.conf import settings
from rest_framework.decorators import api_view
from django.http import JsonResponse

@api_view(['POST'])
def upload_file(request):
    metodo = request.POST.get('metodo')
    if metodo == 'carro':
        if request.FILES.get('file'):
            img = Image.open(request.FILES.get('file'))
            path = os.path.join(settings.MEDIA_ROOT, f'reservas/carros/{request.POST.get('placa')}.jpg')
            img = img.save(path) 
            return JsonResponse({'message': 'Upload com sucesso'}, status=200)
        return JsonResponse({'error': 'Nenhum arquivo enviado'}, status=400)
    elif metodo == 'diario':
        return False
    