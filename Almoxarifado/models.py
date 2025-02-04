# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Colaborador(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    nome = models.CharField(blank=True, null=True)
    cpf = models.CharField(blank=True, null=True)
    rg = models.CharField(blank=True, null=True)
    nascimento = models.DateField(blank=True, null=True)
    fone = models.CharField(blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    equipe = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colaborador'


class EpiCadastro(models.Model):
    produto = models.ForeignKey('Produto', models.DO_NOTHING, db_column='produto')
    ca = models.CharField()
    validade = models.DateField()
    observacao = models.CharField(blank=True, null=True)
    tamanho = models.CharField()
    fabricante = models.CharField()

    class Meta:
        managed = False
        db_table = 'epi_cadastro'


class EpiMovimentacao(models.Model):
    epi_cadastro = models.ForeignKey(EpiCadastro, models.DO_NOTHING, db_column='epi_cadastro')
    quantidade = models.IntegerField()
    colaborador = models.IntegerField()
    obra = models.IntegerField()
    data_entrega = models.DateField()
    baixado = models.BooleanField(blank=True, null=True)
    data_baixa = models.DateField(blank=True, null=True)
    devolvido = models.BooleanField(blank=True, null=True)
    assinado = models.BooleanField(blank=True, null=True)
    ficha = models.ForeignKey('Ficha', models.DO_NOTHING, db_column='ficha', blank=True, null=True)
    papel = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'epi_movimentacao'


class Ficha(models.Model):
    id = models.CharField(primary_key=True)
    colaborador = models.IntegerField()
    pagina = models.IntegerField()
    completa = models.BooleanField(blank=True, null=True)
    url = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ficha'


class Numeracao(models.Model):
    id = models.IntegerField(primary_key=True)
    colaborador = models.IntegerField()
    bota = models.IntegerField(blank=True, null=True)
    botina = models.IntegerField(blank=True, null=True)
    luva = models.CharField(blank=True, null=True)
    camisa = models.CharField(blank=True, null=True)
    calca = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'numeracao'


class Obra(models.Model):
    id = models.IntegerField(primary_key=True)
    orcamento = models.CharField(max_length=20)
    retrabalho = models.CharField(max_length=20, blank=True, null=True)
    empresa = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    descricao = models.CharField(max_length=500, blank=True, null=True)
    finalizada = models.BooleanField()
    indice = models.CharField(max_length=100)
    supervisor = models.CharField(max_length=100, blank=True, null=True)
    tecnicon = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obra'


class Ocupacao(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    colaborador = models.IntegerField(blank=True, null=True)
    funcao = models.CharField(blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    continuo = models.BooleanField(blank=True, null=True)
    terceiro = models.BooleanField(blank=True, null=True)
    equipe = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ocupacao'


class Produto(models.Model):
    produto = models.CharField()
    descricao = models.CharField(blank=True, null=True)
    durabilidade = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produto'
