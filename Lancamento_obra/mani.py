from .models import *
from Home.models import Historico
from django.db import IntegrityError, DatabaseError
from django.core import checks, exceptions, validators


from rest_framework.response import Response
from datetime import datetime


def createHistorico(idr, user, action, context):
        Historico.objects.create(idr=idr, user=user, data=datetime.now(), action=action, context=context)


class mani:
    def __init__(self) -> None:
        pass

    def create(dict,obj):
        try:
            obj.__dict__.update(dict)
            obj.save()
            # pass
        except IntegrityError as e:
            e = str(e)
            if 'null value' in e:
                e = f'Campo "{e.split('DETAIL:')[0].split('"')[1]}", não pode ser vazio'
            elif 'duplicate key' in e:
                e = e.split('DETAIL:')[1].replace('Key', 'Chave').replace('already exists.', 'já existe no banco.')
            return Response({'method':'Integridade','message':e}, status=400)
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
            message = str(e).split('DETAIL:')[0].split('"')[1]
            return Response({'method':'Integridade','message':f'Campo "{message}", não pode ser vazio'}, status=400)
        except DatabaseError as e:
            message = str(e).split('CONTEXT:')[0]
            return Response({'method':'Banco de dados','message': message}, status=400)
        except:
            return Response({'method':'Desconhecido','message':'Update cancelado'},status=400)    
        else:    
            return Response({'method':'Sucesso','message':'Atualização realizado com sucesso!'}, status=200)

