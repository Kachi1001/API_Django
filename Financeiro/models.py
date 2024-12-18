# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Conta(models.Model):
    cod_conta = models.IntegerField(primary_key=True)
    descricao = models.CharField()

    class Meta:
        managed = False
        db_table = 'conta'


class ExtratoBancario(models.Model):
    cod_conta = models.IntegerField()
    data = models.DateField()
    historico = models.CharField()
    debito = models.DecimalField(max_digits=65535, decimal_places=2, blank=True, null=True)
    credito = models.DecimalField(max_digits=65535, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'extrato_bancario'


class SaldoInicial(models.Model):
    cod_conta = models.IntegerField(primary_key=True)
    data = models.DateField()
    valor = models.DecimalField(max_digits=65535, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'saldo_inicial'
