from rest_framework import serializers
from .models import *

        
        
class ColaboradorSerializer(serializers.ModelSerializer):
    # ferias_utilizadas = serializers.StringRelatedField(many=True)
    # ferias_utilizadas = FeriasUtilizadasSerializer(many=True, read_only=True)
    # periodos = PeriodoAquisitivoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Colaborador
        fields = '__all__'  # Ou liste os campos que deseja expor na API  
           

class ColaboradorSelect(serializers.ModelSerializer):
    value = serializers.CharField(source='id')
    text = serializers.CharField(source='nome')

    class Meta:
        model = Colaborador
        fields = ['value','text']  # Ou liste os campos que deseja expor na API    


class PeriodoAquisitivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoAquisitivo
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
class PeriodoAquisitivoTable(serializers.ModelSerializer):
    colaborador = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='nome'
     )
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
    class Meta:
        model = FeriasProcessadas
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
class FeriasProcessadasTable(serializers.ModelSerializer):
    colaborador = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='nome'
     )
    class Meta:
        model = FeriasProcessadas
        fields = '__all__'  # Ou liste os campos que deseja expor na API

        
class FeriasUtilizadasSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeriasUtilizadas
        fields = '__all__'  # Ou liste os campos que deseja expor na API

class FeriasUtilizadasTable(serializers.ModelSerializer):
    colaborador = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='nome'
     )
    class Meta:
        model = FeriasUtilizadas
        fields = '__all__'  # Ou liste os campos que deseja expor na API

   
class OcupacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ocupacao
        fields = '__all__' # Ou liste os campos que deseja expor na API     
        
class LembreteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lembrete
        fields = '__all__' # Ou liste os campos que deseja expor na API     
class FeriadoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feriado
        fields = '__all__' # Ou liste os campos que deseja expor na API     


class AvaliacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Colaborador
        fields = '__all__'  # Ou liste os campos que deseja expor na API  

class AvaliacaoTable(serializers.ModelSerializer):
    avaliacao = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='situacao'
     )
    class Meta:
        model = Colaborador
        fields = '__all__'  # Ou liste os campos que deseja expor na API  

class TipoAvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColabAvaliacao
        fields = '__all__'  # Ou liste os campos que deseja expor na API  


class TipoAvaliacaoSelect(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='situacao')
        
        class Meta:
            model = ColabAvaliacao
            fields = ['value','text']  # Ou liste os campos que deseja expor na API   
    
        
Select = {
        'colaborador': ColaboradorSelect,
        'equipe': EquipeSelect,
        'periodo_aquisitivo': PeriodoAquisitivoSelect,
        'funcao': FuncaoSelect,
        'avaliacao': TipoAvaliacaoSelect,
        'categoria': [{'value':'1'},{'value':'2'},{'value':'3'},{'value':'TERCEIRO'},{'value':'ESTAGIARIO'}],
        'padrao': [{'value':'07:25, 17:55','text':'Colaborador'},{'value':'07:25, 15:25'},{'value':'13:25, 17:25'}],
}    