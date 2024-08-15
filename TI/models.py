# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Adicionais(models.Model):
    servico = models.CharField()
    nome = models.CharField()
    valor = models.CharField()
    data = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adicionais'


class Colaborador(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField()
    admissao = models.DateField(blank=True, null=True)
    setor = models.CharField()
    funcao = models.CharField()

    class Meta:
        managed = False
        db_table = 'colaborador'


class Detalhes(models.Model):
    id = models.BigAutoField(primary_key=True)
    equipamento = models.CharField()
    nome = models.CharField()
    valor = models.CharField()
    data = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalhes'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Equipamentos(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=255)
    tag = models.CharField(blank=True, null=True)
    aquisicao = models.DateField(blank=True, null=True)
    marca = models.CharField(blank=True, null=True)
    modelo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipamentos'


class Estoque(models.Model):
    id = models.BigAutoField(primary_key=True)
    produto = models.CharField()
    quantidade = models.DateField(blank=True, null=True)
    valor_total = models.CharField()
    lote = models.CharField()

    class Meta:
        managed = False
        db_table = 'estoque'


class Padrao(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField()
    valor = models.DateField(blank=True, null=True)
    relacionado = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'padrao'


class Produtos(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField()
    marca = models.DateField(blank=True, null=True)
    descricao = models.CharField()
    equipamento = models.CharField()
    unidade = models.CharField()
    estoque_min = models.CharField()

    class Meta:
        managed = False
        db_table = 'produtos'


class Servicos(models.Model):
    id = models.BigAutoField(primary_key=True)
    servico = models.CharField()
    responsavel = models.DateField(blank=True, null=True)
    data_realizacao = models.CharField()
    data_pedido = models.CharField()
    tag = models.CharField()
    descricao = models.CharField()

    class Meta:
        managed = False
        db_table = 'servicos'
