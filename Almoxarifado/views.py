from django.db import models

class Repor(models.Model):
    id_colab = models.IntegerField(primary_key=True)
    nome = models.CharField()
    funcao = models.CharField()
    id_produto = models.IntegerField()
    produto = models.CharField()
    tamanho = models.CharField()
    reposicao = models.DateField()
    situacao = models.CharField()

    class Meta:
        managed = False
        db_table = 'repor'

class Baixar(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField()
    produto = models.CharField()
    ca = models.CharField()
    validade = models.DateField()
    tamanho = models.CharField()
    quantidade = models.IntegerField()
    fabricante = models.CharField()
    observacao = models.CharField()
    obra = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'baixar'

class Assinar(models.Model):
    id_colab = models.IntegerField(primary_key=True)
    colaborador = models.CharField()
    novos_produtos = models.CharField()
    data_entrega = models.DateField()

    class Meta:
        managed = False
        db_table = 'assinar'