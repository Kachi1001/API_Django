# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AgendaCarros(models.Model):
    id = models.BigAutoField(primary_key=True)
    carro = models.CharField(max_length=100)
    data = models.DateField()
    responsavel = models.CharField(max_length=20)
    destino = models.CharField(max_length=10, blank=True, null=True)
    reservado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agenda_carros'


class AgendaSalas(models.Model):
    id = models.BigAutoField(primary_key=True)
    sala = models.CharField(max_length=100)
    data = models.DateField()
    responsavel = models.CharField(max_length=20)
    reservado = models.CharField(max_length=20, blank=True, null=True)
    hora = models.CharField(max_length=10, blank=True, null=True)
    descricao = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agenda_salas'


class Carros(models.Model):
    placa = models.CharField(primary_key=True, max_length=9)
    marca = models.CharField(max_length=20, blank=True, null=True)
    modelo = models.CharField(max_length=30, blank=True, null=True)
    imagem = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carros'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
