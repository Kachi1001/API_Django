from django.db import models

class ativos_rotatividade(models.Model):
    cpt = models.CharField(primary_key=True)
    ativos = models.BigIntegerField()
    admissoes = models.BigIntegerField()
    desligamentos = models.BigIntegerField()
    
    class Meta:
        managed = False
        db_table = 'grafico_ativos_rotatividade'
        
class FeriasSaldos(models.Model):
    id = models.IntegerField()
    colaborador = models.CharField(primary_key=True)
    equipe = models.CharField()
    adquirido_em = models.DateField()
    data_limite_processar = models.DateField()
    proximidade = models.CharField()
    saldo_escritorio = models.BigIntegerField()
    dias_processados = models.BigIntegerField()
    dias_utilizados = models.BigIntegerField()
    saldo_pf = models.BigIntegerField()
    
    class Meta:
        managed = False
        db_table = 'ferias_saldo'

class FeriasMensagem(models.Model):
    colaborador = models.CharField(primary_key=True)
    equipe = models.CharField()
    gestor = models.CharField()
    fone = models.CharField()
    adquirido_em = models.DateField()
    data_limite_processar = models.DateField()
    proximidade = models.CharField()
    saldo_escritorio = models.BigIntegerField()
    dias_processados = models.BigIntegerField()
    dias_utilizados = models.BigIntegerField()
    saldo_pf = models.BigIntegerField()
    
    class Meta:
        managed = False
        db_table = 'ferias_mensagem'
        
class EpiNr(models.Model):
    id = models.IntegerField(primary_key=True)
    colaborador = models.CharField()
    tipo = models.CharField()
    emitido = models.BooleanField()
    validade = models.DateField()
    observacao = models.CharField()
    
    class Meta:
        managed = False
        db_table = 'epi_nr'
        
class Lembrete2(models.Model):
    nome = models.CharField(primary_key=True)
    horario_padrao = models.CharField()
    fone = models.CharField()

    class Meta:
        managed = False
        db_table = 'lembrete_'
        
        
