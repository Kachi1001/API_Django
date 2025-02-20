from django.db import models

class resumo(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    funcao_pretendida = models.CharField(max_length=255)
    pretensao = models.IntegerField()
    banco_talentos = models.CharField(max_length=255)
    ficha = models.BooleanField()
    disponibilidade = models.BooleanField()
    anos_exp = models.IntegerField()
    avaliacao_final = models.CharField(max_length=255)
    experiencia = models.CharField(max_length=255)
    revisar_dp = models.BooleanField()
    
    class Meta:
        managed = False
        db_table = 'resumo'
        
class pontuacao_experiencias(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    anos_exp = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    subarea = models.IntegerField()
    banco_talentos = models.CharField(max_length=255)
    disponibilidade = models.BooleanField()
    ficha = models.BooleanField()
    experiencia = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'pontuacao_experiencias'

class revisar(models.Model):
    candidato = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    revisar_experiencias = models.IntegerField(max_length=255)
    sub_area = models.CharField()
    
    class Meta:
        managed = False
        db_table = 'revisar'

class IndicacoesExternas(models.Model):
    indicacao = models.CharField(max_length=255)
    candidato = models.CharField()
    data_recebimento = models.DateField()    
    situacao = models.CharField()
    data_finalizacao = models.DateField()    
    observacao = models.CharField()
    
    class Meta:
        managed = False
        db_table = 'indicacoes_externas'

