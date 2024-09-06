from django.db import models

class Incompletos(models.Model):
    dia = models.DateField(primary_key=True)
    nome = models.CharField()
    total_horas = models.DurationField()
    encarregado = models.CharField()
    obra = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'incompletos'
        
class HoraMes(models.Model):
    competencia = models.CharField(primary_key=True)
    colaborador = models.CharField()
    folgas = models.DurationField()
    faltas = models.DurationField()
    dispensas = models.DurationField()
    he50 = models.DurationField()
    he100 = models.DurationField()

    class Meta:
        managed = False
        db_table = 'horas_mes'
