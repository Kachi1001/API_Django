from django.db import models

class hora_extra(models.Model):
    mes = models.CharField(primary_key=True)
    hora_50 = models.DurationField()
    hora_100 = models.DurationField()
    
    def hora_50int(self):
        return int(self.hora_50)
    
    class Meta:
        managed = False
        db_table = 'grafico_hora_extra'
        
class resumo_cidade(models.Model):
    cidade = models.CharField(primary_key=True)
    empresa = models.CharField()
    total_horas = models.DurationField()

    class Meta:
        managed = False
        db_table = 'grafico_empresa_cidade'