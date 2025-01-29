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
    candidato = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    nota = models.IntegerField()
    setor = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'pontuacao_experiencias'

