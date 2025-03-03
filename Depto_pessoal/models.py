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


class AdicionaisFolha(models.Model):
    colaborador = models.ForeignKey('Colaborador', models.DO_NOTHING, db_column='colaborador')
    competencia = models.CharField(max_length=7)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    descricao = models.CharField(blank=True, null=True)
    horas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    minutos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    desconto = models.BooleanField(blank=False, null=False)
    intervalo = models.DurationField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'adicionais_folha'
        
class AdicionaisTrabalhista(models.Model):
    id = models.DateField(primary_key=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    descricao = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adicionais_trabalhista'


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


class Atividade(models.Model):
    colaborador = models.CharField(max_length=255)
    dia = models.DateField()
    descricao = models.CharField(max_length=600, blank=True, null=True)
    indice = models.IntegerField()
    diaseguinte = models.BooleanField()
    horaini1 = models.TimeField()
    horafim1 = models.TimeField()
    horaini2 = models.TimeField(blank=True, null=True)
    horafim2 = models.TimeField(blank=True, null=True)
    horaini3 = models.TimeField(blank=True, null=True)
    horafim3 = models.TimeField(blank=True, null=True)
    perdevale = models.BooleanField(blank=True, null=True)
    revisaorh = models.CharField(max_length=255, blank=True, null=True)
    etapa1 = models.IntegerField(blank=True, null=True)
    etapa2 = models.IntegerField(blank=True, null=True)
    etapa3 = models.IntegerField(blank=True, null=True)
    atividade = models.CharField(max_length=30)
    obra = models.IntegerField()
    diario = models.CharField(max_length=30, blank=True, null=True)
    meiadiaria = models.BooleanField(blank=True, null=True)
    supervisor = models.CharField(max_length=100, blank=True, null=True)
    motivo = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atividade'


class AtividadeHoras(models.Model):
    colaborador = models.CharField(blank=True, null=True)
    dia = models.DateField(blank=True, null=True)
    obra = models.IntegerField(blank=True, null=True)
    hn = models.TimeField(blank=True, null=True)
    h50 = models.TimeField(blank=True, null=True)
    h100 = models.TimeField(blank=True, null=True)
    competencia = models.CharField(blank=True, null=True)
    dispensa = models.TimeField(blank=True, null=True)
    falta = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atividade_horas'


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
    colab_avaliacao = models.ForeignKey(ColabAvaliacao, models.DO_NOTHING, db_column='colab_avaliacao', blank=True, null=True)
    avaliacao_descricao = models.CharField(blank=True, null=True)
    avaliacao_recontratar = models.BooleanField(blank=True, null=True)
    pasta_servidor = models.CharField(blank=True, null=True)
    aviso_ponto = models.BooleanField(blank=True, null=True)
    ctps = models.CharField(blank=True, null=True)
    rg_emissor = models.CharField(blank=True, null=True)

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


class Diarias(models.Model):
    colaborador = models.CharField(max_length=255, blank=True, null=True)
    competencia = models.TextField(blank=True, null=True)
    diaria = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_diarias = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_horas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    horas = models.DurationField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diarias'


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
    adicional = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    total = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

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


class HorasMes(models.Model):
    competencia = models.TextField(blank=True, null=True)
    colaborador = models.CharField(max_length=255, blank=True, null=True)
    contrato = models.CharField(max_length=20, blank=True, null=True)
    folgas = models.DurationField(blank=True, null=True)
    faltas = models.DurationField(blank=True, null=True)
    dispensas = models.DurationField(blank=True, null=True)
    he50 = models.DurationField(blank=True, null=True)
    he100 = models.DurationField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'horas_mes'


class HorasPonto(models.Model):
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')
    extras = models.DurationField()
    data = models.DateField()

    class Meta:
        managed = False
        db_table = 'horas_ponto'


class HorasTotais(models.Model):
    colaborador = models.CharField(blank=True, null=True)
    competencia = models.TextField(blank=True, null=True)
    hn = models.DurationField(blank=True, null=True)
    h50 = models.DurationField(blank=True, null=True)
    h100 = models.DurationField(blank=True, null=True)
    disp = models.DurationField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'horas_totais'


class Inconsistencias(models.Model):
    colaborador = models.CharField(max_length=255, blank=True, null=True)
    dia = models.DateField(blank=True, null=True)
    atestados = models.DurationField(blank=True, null=True)
    dispensas = models.DurationField(blank=True, null=True)
    faltas = models.DurationField(blank=True, null=True)
    ferias = models.DurationField(blank=True, null=True)
    folgas = models.DurationField(blank=True, null=True)
    treinamento = models.DurationField(blank=True, null=True)
    atividade = models.DurationField(blank=True, null=True)
    total = models.DurationField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inconsistencias'


class Insalubridade(models.Model):
    id = models.DateField(primary_key=True)
    valor = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'insalubridade'


class Integracao(models.Model):
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')
    validade = models.DateField(default=None)
    descricao = models.CharField(blank=True, null=True)
    data_integracao = models.DateField(blank=True, null=True)
    empresa = models.CharField()

    class Meta:
        managed = False
        db_table = 'integracao'


class IntegracaoEpi(models.Model):
    id = models.IntegerField(primary_key=True)
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')
    aso = models.BooleanField()
    aso_valid = models.DateField(blank=True, null=True)
    os = models.BooleanField()
    os_valid = models.DateField(blank=True, null=True)
    observacao = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'integracao_aso'


class IntegracaoNr(models.Model):
    integracao_nr_tipo = models.ForeignKey('IntegracaoNrTipo', models.DO_NOTHING, db_column='integracao_nr_tipo')
    emissao = models.DateField()
    validade = models.DateField(null=True, blank=True)
    colaborador = models.ForeignKey(Colaborador, models.DO_NOTHING, db_column='colaborador')
    observacao = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'integracao_nr'


class IntegracaoNrTipo(models.Model):
    id = models.CharField(primary_key=True)
    validade = models.IntegerField()

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


class Localizacaoprogramada(models.Model):
    colaborador = models.CharField(max_length=255)
    iniciosemana = models.DateField()
    encarregado = models.CharField(max_length=100, blank=True, null=True)
    observacao = models.CharField(max_length=255, blank=True, null=True)
    obra = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'localizacaoprogramada'


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
