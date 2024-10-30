from rest_framework import serializers
from .models import *

        
        
class ColaboradorSerializer(serializers.ModelSerializer):
    # ferias_utilizadas = serializers.StringRelatedField(many=True)
    # ferias_utilizadas = FeriasUtilizadasSerializer(many=True, read_only=True)
    # periodos = PeriodoAquisitivoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Colaborador
        fields = '__all__'  # Ou liste os campos que deseja expor na API  
           
class ColabNomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = ['nome','id']

class ColaboradorSelect(serializers.ModelSerializer):
    value = serializers.CharField(source='id')
    text = serializers.CharField(source='nome')

    class Meta:
        model = Colaborador
        fields = ['value','text']  # Ou liste os campos que deseja expor na API    


class PeriodoAquisitivoSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='id')
    colaborador = ColabNomeSerializer(many=False, read_only=True)
    
    class Meta:
        model = PeriodoAquisitivo
        fields = '__all__'  # Ou liste os campos que deseja expor na API
                   
class PeriodoAquisitivoSelect(serializers.ModelSerializer):
    class Meta:
        model = PeriodoAquisitivo
        fields = '__all__'  # Ou liste os campos que deseja expor na API 

class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = '__all__'  # Ou liste os campos que deseja expor na API     

class EquipeSelect(serializers.ModelSerializer):
    value = serializers.CharField(source='id')

    class Meta:
        model = Equipe
        fields = ['value']  # Ou liste os campos que deseja expor na API     

class FuncaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcao
        fields = '__all__'  # Ou liste os campos que deseja expor na API 
        
class FuncaoSelect(serializers.ModelSerializer):
    value = serializers.CharField(source='id')

    class Meta:
        model = Funcao
        fields = ['value']  # Ou liste os campos que deseja expor na API 
                
class FeriasProcessadasSerializer(serializers.ModelSerializer):
    colaborador = ColabNomeSerializer(many=False, read_only=False)
    
    class Meta:
        model = FeriasProcessadas
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
class FeriasUtilizadasSerializer(serializers.ModelSerializer):
    colaborador = ColabNomeSerializer(many=False, read_only=False)
    
    class Meta:
        model = FeriasUtilizadas
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    
   
class OcupacaoSerializer(serializers.ModelSerializer):
    # funcao = FuncaoSerializer(many=False)

    
    class Meta:
        model = Ocupacao
        fields = '__all__' # Ou liste os campos que deseja expor na API     
        
class LembreteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lembrete
        fields = '__all__' # Ou liste os campos que deseja expor na API     
        
