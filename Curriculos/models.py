# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Anexos(models.Model):
    id = models.CharField(primary_key=True)
    candidato = models.ForeignKey('Candidato', models.DO_NOTHING, db_column='candidato')
    nome = models.CharField()
    link = models.CharField(blank=True, null=True)
    tipo = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anexos'


class AreaAtuacao(models.Model):
    area = models.CharField()

    class Meta:
        managed = False
        db_table = 'area_atuacao'


class AvaliacaoTipo(models.Model):
    id = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'avaliacao_tipo'


class Candidato(models.Model):
    nome = models.CharField()
    cpf = models.CharField(blank=True, null=True)
    rg = models.CharField(blank=True, null=True)
    cnh = models.ForeignKey('Cnh', models.DO_NOTHING, db_column='cnh', blank=True, null=True)
    telefone = models.CharField(blank=True, null=True)
    telefone2 = models.CharField(blank=True, null=True)
    nascimento = models.DateField(blank=True, null=True)
    estado_civil = models.ForeignKey('EstadoCivil', models.DO_NOTHING, db_column='estado_civil', blank=True, null=True)
    filho = models.BooleanField(blank=True, null=True)
    endereco = models.CharField(blank=True, null=True)
    bairro = models.CharField(blank=True, null=True)
    cidade = models.CharField(blank=True, null=True)
    data_cadastro = models.DateField(blank=True, null=True)
    indicacao = models.CharField(max_length=255, blank=True, null=True)
    idade = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    estado = models.ForeignKey('Estados', models.DO_NOTHING, db_column='estado', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'candidato'


class Classificacao(models.Model):
    candidato = models.IntegerField()
    area_atuacao = models.ForeignKey(AreaAtuacao, models.DO_NOTHING, db_column='area_atuacao')
    setor = models.ForeignKey('Setor', models.DO_NOTHING, db_column='setor', blank=True, null=True)
    pontos = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classificacao'


class Cnh(models.Model):
    id = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'cnh'


class Conversao(models.Model):
    area_atuacao = models.ForeignKey(AreaAtuacao, models.DO_NOTHING, db_column='area_atuacao')
    area_relacionada = models.ForeignKey(AreaAtuacao, models.DO_NOTHING, db_column='area_relacionada', related_name='conversao_area_relacionada_set')
    porcentagem = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'conversao'


class Entrevista(models.Model):
    candidato = models.ForeignKey(Candidato, models.DO_NOTHING, db_column='candidato')
    profissao = models.ForeignKey('Profissoes', models.DO_NOTHING, db_column='profissao')
    pretensao = models.DecimalField(max_digits=7, decimal_places=2)
    banco_talentos = models.ForeignKey('EntrevistaClassificacao', models.DO_NOTHING, db_column='banco_talentos')
    avaliacao_final = models.CharField()
    revisar_periodo = models.BooleanField(blank=True, null=True)
    data_cadastro = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entrevista'


class EntrevistaClassificacao(models.Model):
    id = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'entrevista_classificacao'


class Escolaridade(models.Model):
    candidato = models.ForeignKey(Candidato, models.DO_NOTHING, db_column='candidato')
    escolaridade = models.ForeignKey('EscolaridadeTipo', models.DO_NOTHING, db_column='escolaridade')
    detalhe = models.CharField(blank=True, null=True)
    conclusao = models.DateField(blank=True, null=True)
    data_cadastro = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'escolaridade'


class EscolaridadeTipo(models.Model):
    id = models.CharField(primary_key=True)
    indice = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'escolaridade_tipo'


class EstadoCivil(models.Model):
    id = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'estado_civil'


class Estados(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    nome = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estados'


class Experiencia(models.Model):
    candidato = models.ForeignKey(Candidato, models.DO_NOTHING, db_column='candidato')
    empresa = models.CharField()
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    tempo_anos = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    tempo_servico = models.CharField(blank=True, null=True)
    profissao = models.ForeignKey('Profissoes', models.DO_NOTHING, db_column='profissao')
    revisar = models.BooleanField(blank=True, null=True)
    data_cadastro = models.DateField(blank=True, null=True)
    area_atuacao = models.ForeignKey(AreaAtuacao, models.DO_NOTHING, db_column='area_atuacao')

    class Meta:
        managed = False
        db_table = 'experiencia'


class Percepcao(models.Model):
    candidato = models.ForeignKey(Candidato, models.DO_NOTHING, db_column='candidato')
    percepcao = models.CharField(blank=True, null=True)
    pesquisa_rh = models.BooleanField()
    origem = models.CharField()
    digitalizacao = models.CharField(blank=True, null=True)
    recebido_em = models.DateField(blank=True, null=True)
    consulta = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'percepcao'


class Profissoes(models.Model):
    funcao = models.CharField()

    class Meta:
        managed = False
        db_table = 'profissoes'


class Questionario(models.Model):
    candidato = models.IntegerField()
    funcionario_antigo = models.BooleanField()
    disponibilidade = models.BooleanField()
    fumante = models.BooleanField()
    bebidas = models.CharField(blank=True, null=True)
    medicacao = models.CharField(blank=True, null=True)
    acidente = models.CharField(blank=True, null=True)
    processo = models.CharField(blank=True, null=True)
    bo = models.CharField(blank=True, null=True)
    criminais = models.CharField(blank=True, null=True)
    policiais = models.CharField(blank=True, null=True)
    judicial = models.CharField(blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    consulta = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'questionario'


class Setor(models.Model):
    setor = models.CharField()

    class Meta:
        managed = False
        db_table = 'setor'
