from rest_framework import serializers
from .models import *


class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = '__all__'  # Ou liste os campos que deseja expor na API     

class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = '__all__'  # Ou liste os campos que deseja expor na API     
class FuncaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcao
        fields = '__all__'  # Ou liste os campos que deseja expor na API     
class FeriasProcessadasSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeriasProcessadas
        fields = '__all__'  # Ou liste os campos que deseja expor na API     
class FeriasUtilizadasSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeriasUtilizadas
        fields = '__all__'  # Ou liste os campos que deseja expor na API     
class OcupacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ocupacao
        fields = '__all__'  # Ou liste os campos que deseja expor na API     
class PeriodoAquisitivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoAquisitivo
        fields = '__all__'  # Ou liste os campos que deseja expor na API     