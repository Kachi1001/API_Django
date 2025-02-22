from django.db import models

class Incompletos(models.Model):
    dia = models.DateField(primary_key=True)
    nome = models.CharField()
    total_horas = models.DurationField()
    encarregado = models.CharField()
    supervisor = models.CharField()
    obra = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'incompletos'
        
class horas_mes(models.Model):
    competencia = models.CharField(primary_key=True)
    contrato = models.CharField()
    colaborador = models.CharField()
    folgas = models.DurationField()
    faltas = models.DurationField()
    dispensas = models.DurationField()
    he50 = models.DurationField()
    he100 = models.DurationField()

    class Meta:
        managed = False
        db_table = 'horas_mes'

class DescontosResumo(models.Model):
    id = models.BigAutoField(primary_key=True)
    responsavel = models.CharField()
    colaborador = models.CharField()
    diario = models.CharField()
    dia = models.DateField()
    folgas = models.DurationField()
    faltas = models.DurationField()
    dispensas = models.DurationField()
    
    class Meta:
        managed = False
        db_table = 'descontos_resumo'
        


class Tecnicon(models.Model):
    tecnicon = models.CharField(primary_key=True)
    lanc_colab = models.CharField()
    lanc_data = models.DateField()
    lanc_descricao = models.CharField()
    lanc_horaini1 = models.CharField()
    lanc_horafim1 = models.CharField()
    lanc_horaini2 = models.CharField()
    lanc_horafim2 = models.CharField()
    lanc_horaini3 = models.CharField()
    lanc_horafim3 = models.CharField()
    lanc_atividade = models.CharField()
    lancado = models.CharField()

    class Meta:
        managed = False
        ordering = ["-tecnicon", 'lanc_colab']
        db_table = 'tecnicon'

class Alocacoes(models.Model):
    tecnicon = models.CharField(primary_key=True)
    colaborador = models.CharField()
    obra = models.IntegerField()
    dia_ini = models.DateField()
    data_fim = models.DateField()

    class Meta:
        managed = False
        db_table = 'alocacoes'
        
class DiariasOk(models.Model):
    colaborador = models.CharField(max_length=255, blank=True, primary_key=True)
    competencia = models.TextField(blank=True, null=True)
    diarias = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    valor_diaria = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    total_diarias = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    horas = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    valor_horas = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    valor_total = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diarias_ok'


class Indicadores(models.Model):
    competencia = models.CharField(primary_key=True)
    indice = models.CharField()
    numeric = models.IntegerField()
    
    class Meta:
        db_table = 'indicadores'
        managed = False

class Fechamento_Revisao(models.Model):
    obra = models.IntegerField(blank=True, null=False, primary_key=True)
    orcamento = models.CharField(max_length=20, blank=True, null=True)
    descricao = models.CharField(max_length=500, blank=True, null=True)
    horas_normais = models.DurationField(blank=True, null=True)
    horas_extra_50 = models.DurationField(blank=True, null=True)
    horas_extra_100 = models.DurationField(blank=True, null=True)
    total_horas = models.DurationField(blank=True, null=True)
    valor_normal = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    valor_extra_50 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    valor_extra_100 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    total_rs = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    revisao = models.TextField(blank=True, null=True)
    nomes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fechamento'

