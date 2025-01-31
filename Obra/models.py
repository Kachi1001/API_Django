# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
# Unable to inspect table 'alocacoes'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'atividade'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'atividade_horas'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'base_terceiros'
# The error was: user mapping not found for "dev_api"


class Cidade(models.Model):
    cidade = models.CharField()
    estado = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'cidade'
# Unable to inspect table 'colaborador'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'colaborador_'
# The error was: user mapping not found for "dev_api"


class CotComposicao(models.Model):
    nome = models.CharField()
    padrao = models.CharField()

    class Meta:
        managed = False
        db_table = 'cot_composicao'


class CotMaterialComposicao(models.Model):
    composicao = models.ForeignKey(CotComposicao, models.DO_NOTHING, db_column='composicao')
    material = models.ForeignKey('MatProduto', models.DO_NOTHING, db_column='material')
    unidade = models.CharField()
    rendimento = models.DecimalField(max_digits=65535, decimal_places=65535)
    espessura = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sn_espessura = models.BooleanField()
    largura = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sn_largura = models.BooleanField()
    comprimento = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sn_comprimento = models.BooleanField()
    outra_dimensao = models.BooleanField()
    desconto_dimensao = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'cot_material_composicao'


class CustoAdm(models.Model):
    competencia = models.CharField(primary_key=True, max_length=7)
    valor = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'custo_adm'
# Unable to inspect table 'descontos_resumo'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'dia'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'diarias'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'diarioobra'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'django_migrations'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'efetividade'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'etapa'
# The error was: user mapping not found for "dev_api"


class FdCompra(models.Model):
    obra = models.IntegerField()
    nf = models.CharField()
    fornecedor = models.ForeignKey('MatFornecedor', models.DO_NOTHING, db_column='fornecedor')
    produto = models.ForeignKey('MatProduto', models.DO_NOTHING, db_column='produto')
    quantidade = models.DecimalField(max_digits=65535, decimal_places=65535)
    valor_unitario = models.DecimalField(max_digits=65535, decimal_places=65535)
    valor_total = models.DecimalField(max_digits=65535, decimal_places=65535)
    observacao = models.CharField(blank=True, null=True)
    bm = models.CharField(blank=True, null=True)
    cancelamento = models.BooleanField()
    unidade = models.CharField(max_length=5)
    data = models.DateField()
    email = models.BooleanField()
    boleto = models.BooleanField()
    vencimento = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fd_compra'


class FdOrcado(models.Model):
    orcamento = models.ForeignKey('Orcamento', models.DO_NOTHING, db_column='orcamento')
    fornecedor = models.ForeignKey('MatFornecedor', models.DO_NOTHING, db_column='fornecedor', blank=True, null=True)
    produto = models.ForeignKey('MatProduto', models.DO_NOTHING, db_column='produto')
    quantidade = models.DecimalField(max_digits=15, decimal_places=6)
    valor_unitario = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    valor_total = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    observacao = models.CharField(blank=True, null=True)
    unidade = models.CharField(max_length=5)
    programado = models.BooleanField()
    composicao = models.IntegerField(blank=True, null=True)
    enviar_cotacao = models.BooleanField()
    etapa = models.CharField(blank=True, null=True)
    cidade = models.ForeignKey(Cidade, models.DO_NOTHING, db_column='cidade')
    endereco = models.CharField(blank=True, null=True)
    data = models.DateField()
    urgencia = models.BooleanField()
    devolver_cotacao = models.BooleanField()
    valor_final = models.BooleanField()
    faturado_direto = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'fd_orcado'


class FdProgramacaoCompra(models.Model):
    obra = models.ForeignKey('Obra', models.DO_NOTHING, db_column='obra')
    fornecedor = models.ForeignKey('MatFornecedor', models.DO_NOTHING, db_column='fornecedor', blank=True, null=True)
    produto = models.ForeignKey('MatProduto', models.DO_NOTHING, db_column='produto')
    quantidade = models.DecimalField(max_digits=65535, decimal_places=65535)
    valor_unitario = models.DecimalField(max_digits=65535, decimal_places=65535)
    valor_total = models.DecimalField(max_digits=65535, decimal_places=65535)
    observacao = models.CharField(blank=True, null=True)
    unidade = models.CharField(max_length=5)
    aquisicao_finalizada = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'fd_programacao_compra'


class FdSobras(models.Model):
    obra = models.IntegerField()
    produto = models.IntegerField()
    quantidade = models.DecimalField(max_digits=65535, decimal_places=65535)
    custo_unitario = models.DecimalField(max_digits=65535, decimal_places=65535)
    total_sobra = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'fd_sobras'
# Unable to inspect table 'feriado'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'funcao'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'grafico'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'horas_mes'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'horas_totais'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'incompletos'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'inconsistencias'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'indicadores'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'indiceobra'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'localizacaoprogramada'
# The error was: user mapping not found for "dev_api"


class MatCategoria(models.Model):
    categoria = models.CharField()
    descricao = models.CharField()

    class Meta:
        managed = False
        db_table = 'mat_categoria'


class MatEpiCadastro(models.Model):
    produto = models.ForeignKey('MatProduto', models.DO_NOTHING, db_column='produto')
    ca = models.CharField()
    validade = models.DateField()
    observacao = models.CharField(blank=True, null=True)
    tamanho = models.CharField()
    fabricante = models.CharField()

    class Meta:
        managed = False
        db_table = 'mat_epi_cadastro'


class MatEpiMovimentacao(models.Model):
    epi = models.ForeignKey('MatProduto', models.DO_NOTHING, db_column='epi')
    quantidade = models.DecimalField(max_digits=65535, decimal_places=65535)
    colaborador = models.IntegerField()
    cr = models.ForeignKey('Obra', models.DO_NOTHING, db_column='cr')
    data_entrega = models.DateField()
    baixado = models.BooleanField()
    data_baixa = models.DateField(blank=True, null=True)
    devolvido = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mat_epi_movimentacao'


class MatFornecedor(models.Model):
    nome = models.CharField()
    cnpj = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mat_fornecedor'


class MatProduto(models.Model):
    produto = models.CharField()
    categoria = models.CharField(blank=True, null=True)
    descricao = models.CharField(blank=True, null=True)
    durabilidade = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mat_produto'


class Medicoes(models.Model):
    id = models.CharField(primary_key=True)
    obra = models.ForeignKey('Obra', models.DO_NOTHING, db_column='obra')
    numero = models.IntegerField()
    data = models.DateField(blank=True, null=True)
    observacao = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicoes'
# Unable to inspect table 'obra'
# The error was: user mapping not found for "dev_api"


class Obra(models.Model):
    id = models.IntegerField(primary_key=True)
    orcamento = models.CharField()
    retrabalho = models.CharField(blank=True, null=True)
    cliente = models.CharField()
    cidade = models.CharField()
    descricao = models.CharField()
    segmento = models.CharField(blank=True, null=True)
    supervisor = models.CharField(blank=True, null=True)
    indice = models.CharField(blank=True, null=True)
    finalizado = models.BooleanField()
    tecnicon = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obra_'


class Orcado(models.Model):
    id = models.OneToOneField(Obra, models.DO_NOTHING, db_column='id', primary_key=True)
    execucao_dias = models.DecimalField(max_digits=65535, decimal_places=65535)
    execucao_horas = models.DecimalField(max_digits=65535, decimal_places=65535)
    fat_direto = models.DecimalField(max_digits=15, decimal_places=2)
    mat_tecnika = models.DecimalField(max_digits=65535, decimal_places=65535)
    maquinas = models.DecimalField(max_digits=65535, decimal_places=65535)
    mo = models.DecimalField(max_digits=65535, decimal_places=65535)
    diversas = models.DecimalField(max_digits=65535, decimal_places=65535)
    impostos = models.DecimalField(max_digits=65535, decimal_places=65535)
    adm_comercial = models.DecimalField(max_digits=65535, decimal_places=65535)
    venda_geral = models.DecimalField(max_digits=65535, decimal_places=65535)
    faturamento = models.DecimalField(max_digits=65535, decimal_places=65535)
    lucro = models.DecimalField(max_digits=65535, decimal_places=65535)
    resultado_p100 = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'orcado'


class OrcadoRealizado(models.Model):
    orcado = models.DecimalField(max_digits=15, decimal_places=2)
    realizado = models.DecimalField(max_digits=15, decimal_places=2)
    tipo = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'orcado_realizado'


class Orcamento(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    cliente = models.CharField()
    cidade = models.ForeignKey(Cidade, models.DO_NOTHING, db_column='cidade', db_comment='foreign key')

    class Meta:
        managed = False
        db_table = 'orcamento'


class Realizado(models.Model):
    id = models.OneToOneField(Obra, models.DO_NOTHING, db_column='id', primary_key=True)
    r_execucao_dias = models.DecimalField(max_digits=65535, decimal_places=65535)
    r_execucao_horas = models.DecimalField(max_digits=65535, decimal_places=65535)
    r_fat_direto = models.DecimalField(max_digits=15, decimal_places=2)
    r_mat_tecnika = models.DecimalField(max_digits=65535, decimal_places=65535)
    r_maquinas = models.DecimalField(max_digits=65535, decimal_places=65535)
    r_mo = models.DecimalField(max_digits=65535, decimal_places=65535)
    r_diversas = models.DecimalField(max_digits=65535, decimal_places=65535)
    r_impostos = models.DecimalField(max_digits=65535, decimal_places=65535)
    r_adm_comercial = models.DecimalField(max_digits=65535, decimal_places=65535)
    r_venda_geral = models.DecimalField(max_digits=65535, decimal_places=65535)
    r_faturamento = models.DecimalField(max_digits=65535, decimal_places=65535)
    r_lucro = models.DecimalField(max_digits=65535, decimal_places=65535)
    r_resultado_p100 = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'realizado'
# Unable to inspect table 'revisao_terceiros'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'sub'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'subconsulta_lancamento'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'supervisor'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'tecnicon'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'temp'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'temp2'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'temp3'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'temp4'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'temp5'
# The error was: user mapping not found for "dev_api"
# Unable to inspect table 'tipo_atividade'
# The error was: user mapping not found for "dev_api"
