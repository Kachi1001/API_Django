from .serializers import SerializerTipo
from .models import *
from django.db import IntegrityError, transaction
from rest_framework.response import Response
from datetime import datetime

def handle_transaction(func):
    def wrapper(*args, **kwargs):
        try:
            with transaction.atomic():
                return func(*args, **kwargs)
        except IntegrityError as e:
            error_message = str(e)
            return Response({'message': f'Erro: {error_message}'}, status=400)
    return wrapper

def save_historico(idr, user, action, context):
    try:
        Historico.objects.create(
            idr=idr, user=user, data=datetime.now(), action=action, context=context
        )
    except IntegrityError as e:
        error_message = str(e)
        return Response({'message': f'Erro ao registrar histórico: {error_message}'}, status=400)

class Register:
    
    @handle_transaction
    def Funcao(user, parametro):
        funcao = parametro.get('funcao')
        if not funcao:
            return Response({'message': 'Erro ao adicionar função: Não pode ser valor nulo'}, status=400)
        
        func = Funcao.objects.create(funcao=funcao, grupo=parametro.get('grupo'))
        save_historico(idr=0, user=user, action='CREATE', context=f"FUNÇÃO <{func.funcao}> ADICIONADA")
        return Response({'message': 'Cadastrado com sucesso'})

    @handle_transaction
    def Colaborador(user, parametro):
        nome = parametro.get('nome')
        if not nome:
            return Response({'message': 'Erro ao adicionar Colaborador: O nome não pode ser nulo'}, status=400)
        
        admissao = parametro.get('admissao') or None
        diaria = None if parametro.get('contrato') == 'CLT' else parametro.get('diaria')
        
        colab = Colaborador.objects.create(
            nome=nome,
            admissao=admissao,
            demissao=None,
            diaria=diaria,
            observacao=parametro.get('observacao'),
            funcao=parametro.get('funcao'),
            contrato=parametro.get('contrato'),
            encarregado=parametro.get('encarregado'),
        )
        
        save_historico(idr=colab.id, user=user, action='CREATE', context=f"COLABORADOR <{colab.nome}> ADICIONADO")
        return Response({'message': 'Cadastrado com sucesso'})

    @handle_transaction
    def Supervisor(user, parametro):
        supervisor = parametro.get('supervisor')
        if not supervisor:
            return Response({'message': 'Erro ao adicionar supervisor: Não pode ser valor nulo'}, status=400)
        
        sup = Supervisor.objects.create(supervisor=supervisor, ativo=parametro.get('ativo'))
        save_historico(idr=0, user=user, action='CREATE', context=f"SUPERVISOR <{sup.supervisor}> ADICIONADO")
        return Response({'message': 'Cadastrado com sucesso'})

    @handle_transaction
    def Carro(user, parametro):
        placa = parametro.get('placa')
        if placa:
            c = Carros.objects.create(placa=parametro.get('placa'), modelo=parametro.get('modelo'),marca=parametro.get('marca'))
            save_historico(idr=0, user=user, action='CREATE', context=f"CARRO <{c.placa}> ADICIONADO")
            return Response({'message': 'Cadastrado com sucesso'})
        else:
            return Response({'message': f'Erro ao adicionar carro: Placa não pode ser nulo'}, status=400)


class Edit:

    @handle_transaction
    def Colaborador(user, parametro):
        nome = parametro.get('nome')
        if not nome:
            return Response({'message': 'Erro ao salvar Colaborador: O nome não pode ser nulo'}, status=400)
        
        colab = Colaborador.objects.get(id=parametro['id'])
        nomeOLD = colab.nome
        
        colab.nome = nome
        colab.admissao = parametro.get('admissao') or colab.admissao
        colab.demissao = parametro.get('demissao') or colab.demissao
        colab.diaria = parametro.get('diaria')
        colab.observacao = parametro.get('observacao')
        colab.funcao = parametro.get('funcao')
        colab.contrato = parametro.get('contrato')
        colab.encarregado = parametro.get('encarregado')
        colab.save()
        
        save_historico(idr=colab.id, user=user, action='UPDATE', context=f"COLABORADOR <{nomeOLD}> EDITADO PARA <{colab.nome}>")
        return Response({'message': 'Atualizado com sucesso'})
    
    @handle_transaction
    def Obra(user, parametro):
        obra = Obra.objects.get(cr=parametro.get('cr'))
        obra.empresa = parametro.get('empresa')
        obra.cidade = parametro.get('cidade')
        obra.descricao = parametro.get('descricao')
        obra.finalizada = parametro.get('finalizada')
        obra.retrabalho = parametro.get('retrabalho')
        obra.indice = parametro.get('indice')
        obra.orcamento = parametro.get('orcamento')
        obra.supervisor = Supervisor(parametro.get('supervisor'))
        
        obra.save()
        
        save_historico(idr=obra.cr, user=user, action='UPDATE', context=f"OBRA <{obra.empresa}> EDITADO")
        return Response({'message': 'Atualizado com sucesso'})
    
    @handle_transaction
    def Lancamentos(user, parametro):
        lanc = Lancamentos.objects.get(id=parametro.get('id'))
        lanc.dia = parametro.get('dia')
        lanc.descricao = parametro.get('descricao')
        lanc.indice = parametro.get('indice')
        lanc.horaini1 = parametro.get('horaini1') or lanc.horaini1
        lanc.horaini2 = parametro.get('horaini2') or lanc.horaini2
        lanc.horaini3 = parametro.get('horaini3') or lanc.horaini3
        lanc.horafim1 = parametro.get('horafim1') or lanc.horafim1
        lanc.horafim2 = parametro.get('horafim2') or lanc.horafim2
        lanc.horafim3 = parametro.get('horafim3') or lanc.horafim3
        lanc.obra = Obra(cr=parametro.get('obra'))
        lanc.colaborador = parametro.get('colaborador')
        
        lanc.save()
        save_historico(idr=lanc.id, user=user, action='UPDATE', context=f"LANÇAMENTOS EDITADO")
        return Response({'message': 'Atualizado com sucesso'})
        
class Delete:
    
    @handle_transaction
    def Colaborador(user, id):
        colab = Colaborador.objects.get(id=id)
        colab.delete()
        save_historico(idr=id, user=user, action='DELETE', context=f"COLABORADOR <{colab.nome}> FOI EXCLUÍDO")
        return Response({'message': 'Deletado com sucesso'})

    @handle_transaction
    def Funcao(user, id):
        func = Funcao.objects.get(funcao=id)
        func.delete()
        save_historico(idr=0, user=user, action='DELETE', context=f"FUNÇÃO <{id}> FOI EXCLUÍDA")
        return Response({'message': 'Deletado com sucesso'})

    @handle_transaction
    def Supervisor(user, id):
        sup = Supervisor.objects.get(supervisor=id)
        sup.delete()
        save_historico(idr=0, user=user, action='DELETE', context=f"SUPERVISOR <{id}> FOI EXCLUÍDO")
        return Response({'message': 'Deletado com sucesso'})
    
    @handle_transaction
    def Obra(user, id):
        x = Obra.objects.get(cr=id)
        x.delete()
        save_historico(idr=0, user=user, action='DELETE', context=f"OBRA <{id}> FOI EXCLUÍDO")
        return Response({'message': 'Deletado com sucesso'})

    @handle_transaction
    def Lancamentos(user, id):
        x = Lancamentos.objects.get(id=id)
        x.delete()
        save_historico(idr=id, user=user, action='DELETE', context=f"ATIVIDADE EXCLUÍDA")
        return Response({'message': 'Deletado com sucesso'})