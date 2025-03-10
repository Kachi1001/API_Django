from django.db import models

class Repor(models.Model):
    id_colab = models.IntegerField(primary_key=True)
    nome = models.CharField()
    funcao = models.CharField()
    id_produto = models.IntegerField()
    produto = models.CharField()
    tamanho = models.CharField()
    reposicao = models.DateField()
    situacao = models.CharField()

    class Meta:
        managed = False
        db_table = 'repor'

class Baixar(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField()
    produto = models.CharField()
    ca = models.CharField()
    validade = models.DateField()
    tamanho = models.CharField()
    quantidade = models.IntegerField()
    fabricante = models.CharField()
    observacao = models.CharField()
    obra = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'baixar'

class Assinar(models.Model):
    id_colab = models.IntegerField(primary_key=True)
    colaborador = models.CharField()
    novos_produtos = models.CharField()
    data_entrega = models.DateField()

    class Meta:
        managed = False
        db_table = 'assinar'
        
class Papel(models.Model):
    id = models.IntegerField(primary_key=True)
    colaborador = models.CharField()
    cod_produto = models.CharField()
    orientacao = models.CharField()
    nome = models.DateField()
    quantidade = models.CharField()
    produto = models.IntegerField()
    data_retirada = models.DateField()
    data_devolucao = models.DateField()
    fabricante = models.CharField()
    ca = models.CharField()
    validade_ca = models.DateField()
    assinatura = models.CharField()

    class Meta:
        managed = False
        db_table = 'papel'
        
class ColabCompleto(models.Model):
    colaborador = models.IntegerField(primary_key=True)
    nome = models.CharField()
    fone = models.CharField()
    ultima = models.IntegerField()
    completa = models.BooleanField()
    numeracao = models.CharField()
    
    class Meta:
        managed = False
        db_table = 'colab_completo'
        
class EpisValidos(models.Model):
    id_colaborador = models.IntegerField(primary_key=True)
    nome = models.CharField()
    id_produto = models.IntegerField()
    produto = models.CharField()
    tamanho = models.CharField()
    validade_uso = models.DateField()
    validade_ca = models.DateField()
    ca = models.CharField()
    situacao = models.CharField()
    
    class Meta:
        ordering = ['situacao']
        managed = False
        db_table = 'epis_validos'

class CabecalhoFicha(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField()
    funcao = models.CharField()
    rg = models.CharField()
    ctps = models.CharField()
    ficha = models.CharField()
    class Meta:
        managed = False
        db_table = 'cabecalho_ficha'

class Movimentacao(models.Model):
    id = models.IntegerField(primary_key=True)
    colaborador = models.IntegerField()
    ficha = models.IntegerField()
    obra = models.IntegerField()
    data_entrega = models.DateField()
    reposicao = models.DateField()
    produto = models.CharField()
    ca = models.CharField()
    quantidade = models.IntegerField()
    tamanho = models.CharField()

    class Meta:
        managed = False
        db_table = 'movimentacao'

class Digitalizar(models.Model):
    id = models.CharField(primary_key=True)
    colaborador = models.IntegerField()
    nome = models.CharField()
    pagina = models.IntegerField()
    data_finalizado = models.DateField()
    data_digitalizacao = models.DateField()

    class Meta:
        managed = False
        db_table = 'digitalizar'

class Arquivar(models.Model):
    id = models.CharField(primary_key=True)
    nome = models.IntegerField()
    pagina = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'arquivar'

class ValidadeCa(models.Model):
    id = models.IntegerField(primary_key=True)
    produto = models.CharField()
    fabricante = models.CharField()
    ca = models.IntegerField()
    validade = models.DateField()
    situacao = models.CharField()

    class Meta:
        managed = False
        db_table = 'validade_ca'
        
