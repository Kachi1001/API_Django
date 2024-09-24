from .models import *
from Home.models import Historico
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from datetime import datetime

def handle_transaction(func):
    def wrapper(*args, **kwargs):
        try:
            # createHistorico()
            func(*args, **kwargs)
        except IntegrityError as e:
            return Response({'message': f'Erro de integridade: {str(e)}'}, status=400)
        except DatabaseError as e:
            message = str(e).split('CONTEXT:')[0]
            return Response({'method':'Banco de dados','message': message}, status=400)
    return wrapper

def createHistorico(idr, user, action, context):
        Historico.objects.create(idr=idr, user=user, data=datetime.now(), action=action, context=context)


class mani:
    def __init__(self) -> None:
        pass

    def create(dict,obj):
        obj.__dict__.update(dict)
        try:
            obj.save()
            # pass
        except IntegrityError as e:
            return Response({'message': f'Erro de integridade: {str(e)}'}, status=400)
        except DatabaseError as e:
            message = str(e).split('CONTEXT:')[0]
            return Response({'method':'Banco de dados','message': message}, status=400)
        except:
            return Response({'method':'Desconhecido','message':'Registro cancelado'},status=400)    
        else:    
            return Response({'method':'Sucesso','message':'Cadastro efetuado com sucesso!'}, status=200)
    def update(dict,obj):
        obj.__dict__.update(dict)
        try:
            obj.save()
            # pass
        except IntegrityError as e:
            return Response({'message': f'Erro de integridade: {str(e)}'}, status=400)
        except DatabaseError as e:
            message = str(e).split('CONTEXT:')[0]
            return Response({'method':'Banco de dados','message': message}, status=400)
        except:
            return Response({'method':'Desconhecido','message':'Registro cancelado'},status=400)    
        else:    
            return Response({'method':'Sucesso','message':'Atualização realizado com sucesso!'}, status=200)

