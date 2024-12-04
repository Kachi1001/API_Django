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
