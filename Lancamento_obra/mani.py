from .models import *
from API.models import Historico
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from datetime import datetime

def handle_transaction(func):
    def wrapper(*args, **kwargs):
        try:
            # createHistorico()
            func(*args, **kwargs)
            return True
        except IntegrityError as e:
            return Response({'message': f'Erro de integridade: {str(e)}'}, status=400)
        except ObjectDoesNotExist as e:
            return Response({'method': f'Erro de pesquisa','message':'Item não encontrado'}, status=400)
        except DatabaseError as e:
            message = str(e).split('CONTEXT:')[0]
            return Response({'method':'Banco de dados','message': message}, status=400)
    return wrapper

def createHistorico(idr, user, action, context):
        Historico.objects.create(idr=idr, user=user, data=datetime.now(), action=action, context=context)
        
@handle_transaction
def objAtividade(obj, parametro):
    try:
        att = TipoAtividade.objects.get(indice=parametro.get('atividade'))
    except:
        att = TipoAtividade(parametro.get('atividade'))
    obra = int(parametro.get('obra'))
    if obra in [2,3,4,5]:
        enviar = True
    else: enviar = False
    obj.obra = Obra(id=obra)
    obj.atividade = att
    obj.dia = parametro.get('dia')
    obj.indice = parametro.get('indice')
    obj.horaini1 = parametro.get('horaini1')
    obj.horaini2 = parametro.get('horaini2')
    obj.horafim1 = parametro.get('horafim1')
    obj.horafim2 = parametro.get('horafim2') 
    obj.horaini3 = parametro.get('horaini3') if not enviar else None
    obj.horafim3 = parametro.get('horafim3') if not enviar else None
    obj.diaseguinte = parametro.get('diaseguinte')  if not enviar else False
    obj.colaborador = parametro.get('colaborador') or obj.colaborador
    obj.meiadiaria = parametro.get('meiadiaria')  if not enviar else False
    obj.supervisor = parametro.get('supervisor') if enviar else None
    obj.motivo = parametro.get('motivo', '') if enviar else None
    obj.descricao = parametro.get('descricao', '')
    obj.save()
    
@handle_transaction
def objColaborador(obj, parametro):
    obj.nome = parametro.get('nome')
    obj.admissao = parametro.get('admissao') or None
    obj.demissao = parametro.get('demissao')
    obj.diaria = parametro.get('diaria') or 0
    obj.observacao = parametro.get('observacao')
    obj.funcao = parametro.get('funcao')
    obj.contrato = parametro.get('contrato')
    obj.encarregado = parametro.get('encarregado')
    obj.save()

@handle_transaction
def objObra(obj, parametro):
    obj.id = parametro.get('id')
    obj.empresa = parametro.get('empresa')
    obj.cidade = parametro.get('cidade')
    obj.descricao = parametro.get('descricao')
    obj.finalizada = parametro.get('finalizada')
    obj.retrabalho = parametro.get('retrabalho') 
    obj.indice = parametro.get('indice')
    obj.orcamento = parametro.get('orcamento')
    obj.supervisor = Supervisor(parametro.get('supervisor'))
    obj.save()

@handle_transaction
def objDiario(obj,parametro):
    obj.data = parametro.get('data')
    obj.obra = Obra(id=parametro.get('obra'))
    obj.encarregado = parametro.get('encarregado')
    obj.climamanha = parametro.get('climamanha')
    obj.climatarde = parametro.get('climatarde')
    obj.imagem = parametro.get('imagem')
    obj.diario = parametro.get('diario')
    obj.indice = parametro.get('indice')
    obj.descricao = parametro.get('descricao')
    obj.save()

@handle_transaction
def objProgramacao(obj,parametro):
    obj.colaborador = parametro.get('colaborador')
    obj.obra = Obra(id=parametro.get('obra'))
    obj.iniciosemana = parametro.get('iniciosemana')
    obj.encarregado = parametro.get('encarregado')
    obj.observacao = parametro.get('observacao', '')
    obj.save()
    
@handle_transaction    
def objSupervisor(obj,parametro):
    obj.supervisor = parametro.get('supervisor')
    obj.ativo = parametro.get('ativo')
    obj.save()

@handle_transaction
def objFuncao(obj,parametro):
    obj.funcao = parametro.get('funcao')
    obj.grupo = parametro.get('grupo') or 1
    obj.save()
