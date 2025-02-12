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


class ColaboradorEquipamento(models.Model):
    colaborador = models.IntegerField()
    equipamento = models.ForeignKey('Equipamento', models.DO_NOTHING, db_column='equipamento')
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    motivo = models.ForeignKey('MotivoEquipamento', models.DO_NOTHING, db_column='motivo')

    class Meta:
        managed = False
        db_table = 'colaborador_equipamento'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Equipamento(models.Model):
    id = models.CharField(primary_key=True)
    modelo = models.ForeignKey('EquipamentoModelo', models.DO_NOTHING, db_column='modelo')
    data_aquisicao = models.DateField()
    motivo = models.ForeignKey('MotivoEquipamento', models.DO_NOTHING, db_column='motivo')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_baixa = models.DateField(blank=True, null=True)
    garantia = models.DateField(blank=True, null=True)

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


class EquipamentoProduto(models.Model):
    produto = models.ForeignKey('Produto', models.DO_NOTHING, db_column='produto')
    equipamento = models.ForeignKey(Equipamento, models.DO_NOTHING, db_column='equipamento')
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    lista = models.ForeignKey('MotivoProduto', models.DO_NOTHING, db_column='lista')

    class Meta:
        managed = False
        db_table = 'equipamento_produto'


class EquipamentoTipo(models.Model):
    id = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'equipamento_tipo'


class EquipamentoWares(models.Model):
    ware = models.ForeignKey('Wares', models.DO_NOTHING, db_column='ware')
    equipamento = models.ForeignKey(Equipamento, models.DO_NOTHING, db_column='equipamento')
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    motivo = models.ForeignKey('MotivoEquipamento', models.DO_NOTHING, db_column='motivo')

    class Meta:
        managed = False
        db_table = 'equipamento_wares'


class Marca(models.Model):
    marca = models.CharField()

    class Meta:
        managed = False
        db_table = 'marca'


class MotivoEquipamento(models.Model):
    id = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'motivo_equipamento'


class MotivoProduto(models.Model):
    id = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'motivo_produto'


class Produto(models.Model):
    modelo = models.ForeignKey('ProdutoModelo', models.DO_NOTHING, db_column='modelo')
    data_aquisicao = models.DateField()
    data_baixa = models.DateField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    unidade = models.CharField(blank=True, null=True)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produto'


class ProdutoModelo(models.Model):
    marca = models.ForeignKey(Marca, models.DO_NOTHING, db_column='marca')
    modelo = models.CharField()
    tipo = models.ForeignKey('ProdutoTipo', models.DO_NOTHING, db_column='tipo')

    class Meta:
        managed = False
        db_table = 'produto_modelo'


class ProdutoTipo(models.Model):
    tipo = models.CharField()
    categoria = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produto_tipo'


class Wares(models.Model):
    tipo = models.ForeignKey('WaresTipo', models.DO_NOTHING, db_column='tipo')
    descricao = models.CharField(blank=True, null=True)
    adquirido = models.BooleanField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pn_serial = models.CharField(blank=True, null=True)
    data_aquisicao = models.DateField(blank=True, null=True)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wares'


class WaresCategoria(models.Model):
    categoria = models.CharField()
    tipo = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'wares_categoria'


class WaresTipo(models.Model):
    categoria = models.ForeignKey(WaresCategoria, models.DO_NOTHING, db_column='categoria')
    descricao = models.CharField()
    ano = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wares_tipo'
