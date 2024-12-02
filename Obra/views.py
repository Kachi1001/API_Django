from django.db import models
        
class orcamento_cotacao(models.Model):
    obra = models.IntegerField(primary_key=True)
    etapa = models.TextField(max_length=255)
    produto = models.TextField(max_length=255)
    quantidade = models.IntegerField()
    observacao = models.TextField(max_length=255)
    unidade = models.TextField(max_length=255)
    composicao = models.IntegerField()
    enviar_cotacao = models.BooleanField()
    
    class Meta:
        managed = False
        db_table = 'orcamento_cotacao'

class lucratividade(models.Model):
    obra = models.IntegerField(primary_key=True)
    h100 = models.TextField(max_length=255)
    colaborador = models.TextField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'lucratividade'
