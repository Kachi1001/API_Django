# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdicionaisCustos(models.Model):
    id = models.DateField(primary_key=True)
    trabalhista = models.DecimalField(max_digits=10, decimal_places=2)
    epi_uniforme = models.DecimalField(max_digits=10, decimal_places=2)
    vale_transporte = models.DecimalField(max_digits=10, decimal_places=2)
    auxilio_escolar = models.DecimalField(max_digits=10, decimal_places=2)
    serplamed = models.DecimalField(max_digits=10, decimal_places=2)
    seguro_vida = models.DecimalField(max_digits=10, decimal_places=2)
    treinamento_nrs = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'adicionais_custos'


class AdicionalPf(models.Model):
    colaborador = models.ForeignKey('Colaborador', models.DO_NOTHING, db_column='colaborador')
    data_inicial = models.DateField()
    data_final = models.DateField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adicional_pf'


class Alimentacao(models.Model):
    id = models.DateField(primary_key=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'alimentacao'
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
    aviso_ponto = models.BooleanField(blank=True, null=True)

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


class FechamentoMensal(models.Model):
    colaborador = models.CharField(blank=True, null=True)
    competencia = models.TextField(blank=True, null=True)
    h50 = models.DurationField(blank=True, null=True)
    h100 = models.DurationField(blank=True, null=True)
    horas_escritorio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salario_insalub = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    hora = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    dispensas = models.DurationField(blank=True, null=True)
    h50_pf = models.DurationField(blank=True, null=True)
    h100_pf = models.DurationField(blank=True, null=True)
    horas_totais = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_menos_quentes = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    saldo_negativo_acumulado = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    valor_pagar = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fechamento_mensal'


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
    observacao = models.CharField(blank=True, null=True)
    utilizar = models.BooleanField(blank=True, null=True)

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
    observacao = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ferias_utilizadas'


class Funcao(models.Model):
    id = models.CharField(primary_key=True)
    categoria = models.CharField()
    insalubridade = models.BooleanField(blank=True, null=True)
    horario_padrao = models.CharField()

    class Meta:
        managed = False
        db_table = 'funcao_'
# Unable to inspect table 'horas_mes'
# The error was: user mapping not found for "dev_api"


class HorasPonto(models.Model):
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')
    extras = models.DurationField()
    data = models.DateField()

    class Meta:
        managed = False
        db_table = 'horas_ponto'
# Unable to inspect table 'horas_totais'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'inconsistencias'
# The error was: user mapping not found for "dev_api"


class Insalubridade(models.Model):
    id = models.DateField(primary_key=True)
    valor = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'insalubridade'


class Integracao(models.Model):
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')
    obra = models.IntegerField()
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
    observacao = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'integracao_nr'


class IntegracaoNrTipo(models.Model):
    id = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'integracao_nr_tipo'


class Lembrete(models.Model):
    nome = models.CharField()
    horario_padrao = models.CharField()
    fone = models.CharField()

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
    extra = models.BooleanField()

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


class TetoQuinquenio(models.Model):
    id = models.DateField(primary_key=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'teto_quinquenio'


class Ultimo(models.Model):
    max = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ultimo'
