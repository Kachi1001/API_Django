# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class App(models.Model):
    id = models.CharField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'app'
class Menu(models.Model):
    app = models.ForeignKey(App, models.DO_NOTHING, db_column='app', blank=True, null=True)
    nome = models.CharField()

    class Meta:
        managed = False
        db_table = 'menu'


class Submenu(models.Model):
    nome = models.CharField()
    url = models.CharField()
    menu = models.ForeignKey(Menu, models.DO_NOTHING, db_column='menu', blank=True, null=True)
    data = models.DateField()

    class Meta:
        managed = False
        db_table = 'submenu'