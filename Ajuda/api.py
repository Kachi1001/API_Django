import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from . import models, views, serializers
from Site_django import util
    
# Configurações de conexão com o banco de dados PostgreSQL


resources = util.get_resources(models)
table_models = util.get_classes(models)
table_views = util.get_classes(views)
serializer_dicts = util.generate_serializer_dicts(serializers)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def tabela(request, table):
    dicts = table_models
    dicts.update(table_views)
    return util.get_table(request, table, dicts, serializer_dicts['Table'])
    
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def select(request, resource):
    return util.create_select(request, resource, serializer_dicts['Select'])

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def resource(request, name):
    return Response(resources.get(name))


class App_list(util.LC):
    serializer_class = serializers.App
    queryset = serializer_class.Meta.model.objects.all()
class App_detail(util.RUD):
    serializer_class = serializers.App
    queryset = serializer_class.Meta.model.objects.all()

class Menu_list(util.LC):
    serializer_class = serializers.Menu
    queryset = serializer_class.Meta.model.objects.all()
    filterset_fields = ['app']
    
class Menu_detail(util.RUD):
    serializer_class = serializers.Menu
    queryset = serializer_class.Meta.model.objects.all()
from django.utils import timezone
from decouple import config
class Submenu_list(util.LC):
    serializer_class = serializers.Submenu
    queryset = serializer_class.Meta.model.objects.all()
    @util.database_exception
    def create(self, request, *args, **kwargs):
        data = request.data
        reg = models.Submenu.objects.create(
            menu=models.Menu.objects.get(id = data['menu']),
            nome = data['nome'],
            data = timezone.now()
            )
        # img = Image.open(request.FILES['image']).convert('RGB')
        file = request.FILES['file']
        resource = f'Ajuda/'
        path = os.path.join(settings.MEDIA_ROOT, resource)
        file_name = f'{reg.id}.pdf'
        try:
            pdf_path = os.path.join(path, file_name)
            with open(pdf_path, 'wb') as pdf_file:
                for chunk in file.chunks():
                    pdf_file.write(chunk)
        except FileExistsError:
            return Response({'message':'Arquivo já existe!'},status=406)
        except Exception as e:
            reg.delete()
            return Response({'message':f'Erro ao salvar o arquivo {str(e)}'},status=400)
        else:
            reg.url = f'{config('MEDIA_URL')}/{resource}{file_name}'
            reg.save()
            return Response({},status=201) 
        
class Submenu_detail(util.RUD):
    serializer_class = serializers.Submenu
    queryset = serializer_class.Meta.model.objects.all()
    
    @util.database_exception
    def delete(self, request, *args, **kwargs):
        resource = f'Ajuda/'
        path = os.path.join(settings.MEDIA_ROOT, resource)
        file_name = f'{kwargs['pk']}.pdf'
        try:
            os.remove(os.path.join(path, file_name))
        except FileNotFoundError:
            pass
        try:
            models.Submenu.objects.get(id = kwargs['pk']).delete()
        except models.Submenu.DoesNotExist:
                return Response(
                {"banco de dados": 'Esse item já foi deletado'},
                status=500
            ) 
        except Exception as e:
            return Response(
                {"banco de dados": str(e)},
                status=500
            )
        return Response(status=204)     