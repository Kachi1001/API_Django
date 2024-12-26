# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
# Unable to inspect table 'atividade'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'atividade_horas'
# The error was: user mapping not found for "dev_api"


class ColabAvaliacao(models.Model):
    situacao = models.CharField()

    class Meta:
        managed = False
        db_table = 'colab_avaliacao'


class Colaborador(models.Model):
    nome = models.CharField()
    cpf = models.CharField(db_comment='text')
    rg = models.CharField(blank=True, null=True)
    nascimento = models.DateField()
    fone = models.CharField(blank=True, null=True)
    ativo = models.BooleanField()
    equipe = models.CharField(blank=True, null=True)
    avaliacao = models.ForeignKey(ColabAvaliacao, models.DO_NOTHING, db_column='avaliacao', blank=True, null=True)
    avaliacao_descricao = models.CharField(blank=True, null=True)
    avaliacao_recontratar = models.BooleanField(blank=True, null=True)
    pasta_servidor = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colaborador_'


class CustoFolha(models.Model):
    id = models.CharField(primary_key=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'custo_folha'


class Dia(models.Model):
    id = models.DateField(primary_key=True)
    feriado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'dia'
# Unable to inspect table 'diarias'
# The error was: user mapping not found for "dev_api"


class Equipe(models.Model):
    id = models.CharField(primary_key=True)
    gestor = models.CharField(blank=True, null=True)
    fone = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipe'


class Feriado(models.Model):
    id = models.DateField(primary_key=True)
    descricao = models.CharField()
    recorrente = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'feriado'


class FeriasProcessadas(models.Model):
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')
    dias_processados = models.IntegerField()
    data_inicio = models.DateField(blank=True, null=True)
    periodo_aquisitivo = models.ForeignKey('PeriodoAquisitivo', models.DO_NOTHING, db_column='periodo_aquisitivo', blank=True, null=True)
    consumido = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'ferias_processadas'


class FeriasUtilizadas(models.Model):
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')
    dias_utilizados = models.IntegerField()
    data_inicio = models.DateField(blank=True, null=True)
    periodo_aquisitivo = models.ForeignKey('PeriodoAquisitivo', models.DO_NOTHING, db_column='periodo_aquisitivo', blank=True, null=True)
    antecipacao_periodo = models.BooleanField()
    consumido = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'ferias_utilizadas'


class Funcao(models.Model):
    id = models.CharField(primary_key=True)
    categoria = models.CharField()
    insalubridade = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funcao_'
# Unable to inspect table 'horas_mes'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'horas_totais'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'inconsistencias'
# The error was: user mapping not found for "dev_api"


class Integracao(models.Model):
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')
    cr = models.IntegerField()
    validade = models.DateField(blank=True, null=True)
    descricao = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'integracao'


class IntegracaoEpi(models.Model):
    id = models.IntegerField(primary_key=True)
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')
    aso = models.BooleanField()
    aso_valid = models.DateField(blank=True, null=True)
    epi = models.BooleanField()
    epi_valid = models.DateField(blank=True, null=True)
    os = models.BooleanField()
    os_valid = models.DateField(blank=True, null=True)
    observacao = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'integracao_epi'


class IntegracaoNr(models.Model):
    nr = models.ForeignKey('IntegracaoNrTipo', models.DO_NOTHING, db_column='nr')
    validade = models.DateField()
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')

    class Meta:
        managed = False
        db_table = 'integracao_nr'


class IntegracaoNrTipo(models.Model):
    id = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'integracao_nr_tipo'


class Lembrete(models.Model):
    colaborador = models.CharField()
    padrao = models.CharField()
    telefone = models.CharField()

    class Meta:
        managed = False
        db_table = 'lembrete'


class LembreteLog(models.Model):
    hora = models.DateTimeField(blank=True, null=True)
    acao = models.CharField(blank=True, null=True)
    padrao = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lembrete_log'
# Unable to inspect table 'localizacaoprogramada'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'obra'
# The error was: user mapping not found for "dev_api"


class Ocupacao(models.Model):
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')
    funcao = models.ForeignKey(Funcao, models.DO_NOTHING, db_column='funcao')
    remuneracao = models.DecimalField(max_digits=7, decimal_places=2)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    continuo = models.BooleanField()
    terceiro = models.BooleanField()
    diaria = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    equipe = models.ForeignKey(Equipe, models.DO_NOTHING, db_column='equipe')

    class Meta:
        managed = False
        db_table = 'ocupacao'


class PeriodoAquisitivo(models.Model):
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')
    adquirido_em = models.DateField()
    periodo = models.IntegerField()
    consumido = models.BooleanField()
    id = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'periodo_aquisitivo'


class ProximoPeriodo(models.Model):
    colaborador = models.IntegerField()
    inicio = models.DateField()
    proximo_periodo = models.DateField()

    class Meta:
        managed = False
        db_table = 'proximo_periodo'


class TesteHorasQuentes(models.Model):
    colaborador = models.CharField()
    mes = models.DateField()
    competencia = models.CharField(blank=True, null=True)
    hora50 = models.DurationField(blank=True, null=True)
    hora100 = models.DurationField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teste_horas_quentes'


class Ultimo(models.Model):
    max = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ultimo'
