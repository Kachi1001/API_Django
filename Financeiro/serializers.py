from rest_framework import serializers
from . import models

class Conta(serializers.ModelSerializer):
    class Meta:
        model = models.Conta
        fields = '__all__'  # Ou liste os campos que deseja expor na API  
    
        
class Extrato_bancario(serializers.ModelSerializer):
    class Meta:
        model = models.ExtratoBancario
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
