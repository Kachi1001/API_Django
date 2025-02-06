# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
# Unable to inspect table 'colaborador'
# The error was: user mapping not found for "dev_api"


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Equipamento(models.Model):

    class Meta:
        managed = False
        db_table = 'equipamento'


class EquipamentoModelo(models.Model):
    marca = models.ForeignKey('Marca', models.DO_NOTHING, db_column='marca')
    modelo = models.CharField()
    tipo = models.ForeignKey('EquipamentoTipo', models.DO_NOTHING, db_column='tipo')

    class Meta:
        managed = False
        db_table = 'equipamento_modelo'


class EquipamentoTipo(models.Model):
    id = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'equipamento_tipo'


class Marca(models.Model):
    marca = models.CharField()

    class Meta:
        managed = False
        db_table = 'marca'


class Modelo(models.Model):
    marca = models.ForeignKey(Marca, models.DO_NOTHING, db_column='marca')
    modelo = models.CharField()
    tipo = models.ForeignKey('Tipo', models.DO_NOTHING, db_column='tipo')

    class Meta:
        managed = False
        db_table = 'modelo'


class Produto(models.Model):
    modelo = models.IntegerField()
    data_aquisicao = models.DateField()
    data_baixa = models.DateField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    unidade = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produto'


class Tipo(models.Model):
    tipo = models.CharField()
    categoria = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo'
