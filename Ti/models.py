# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Colaborador(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField()
    admissao = models.DateField(blank=True, null=True)
    setor = models.CharField()
    funcao = models.CharField()

    class Meta:
        managed = False
        db_table = 'colaborador'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Maquina(models.Model):
    tipo = models.CharField(max_length=50)
    aquisicao = models.DateField(blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    serial_number = models.CharField(blank=True, null=True)
    descricao = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maquina'


class Padrao(models.Model):
    chave = models.CharField()
    relacionado = models.CharField()

    class Meta:
        managed = False
        db_table = 'padrao'


class Produto(models.Model):
    chave = models.CharField()
    maquina = models.CharField()
    modelo = models.CharField(blank=True, null=True)
    fabricante = models.CharField(blank=True, null=True)
    serial_number = models.CharField(blank=True, null=True)
    custo = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    data_aquisicao = models.DateField(blank=True, null=True)
    data_baixa = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produto'
