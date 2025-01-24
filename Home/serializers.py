from rest_framework import serializers
from . import models


class Pendencia(serializers.ModelSerializer):
    class Meta:
        model = models.Pendencia
        fields = '__all__'  # Ou liste os campos que deseja expor na API  
        
class Log(serializers.ModelSerializer):
    class Meta:
        model = models.Log
        fields = '__all__'  # Ou liste os campos que deseja expor na API  
        