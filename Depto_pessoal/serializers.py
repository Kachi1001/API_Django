from rest_framework import serializers
from . import models
from Obra import serializers as ObraSerializer

from . import views
        
class Colaborador(serializers.ModelSerializer):
    # ferias_utilizadas = serializers.StringRelatedField(many=True)
    # ferias_utilizadas = FeriasUtilizadasSerializer(many=True, read_only=True)
    # periodos = PeriodoAquisitivoSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Colaborador
        fields = '__all__'  # Ou liste os campos que deseja expor na API  
           
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='nome')

        class Meta:
            model = models.Colaborador
            fields = ['value','text','ativo']  # Ou liste os campos que deseja expor na API    
    def Select_ordened():
        return Colaborador.Select(Colaborador.Select.Meta.model.objects.all().order_by('nome'), many=True).data

class PeriodoAquisitivo(serializers.ModelSerializer):
    class Meta:
        model = models.PeriodoAquisitivo
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
    class Table(serializers.ModelSerializer):
        colaborador = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='nome'
        )
        class Meta:
            model = models.PeriodoAquisitivo
            fields = '__all__'  # Ou liste os campos que deseja expor na API

                   
    class Select(serializers.ModelSerializer):
        class Meta:
            model = models.PeriodoAquisitivo
            fields = '__all__'  # Ou liste os campos que deseja expor na API 

class Equipe(serializers.ModelSerializer):
    class Meta:
        model = models.Equipe
        fields = '__all__'  # Ou liste os campos que deseja expor na API     

    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')

        class Meta:
            model = models.Equipe
            fields = ['value']  # Ou liste os campos que deseja expor na API     

class Funcao(serializers.ModelSerializer):
    class Meta:
        model = models.Funcao
        fields = '__all__'  # Ou liste os campos que deseja expor na API 
        
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')

        class Meta:
            model = models.Funcao
            fields = ['value']  # Ou liste os campos que deseja expor na API 
                
class FeriasProcessadas(serializers.ModelSerializer):
    class Meta:
        model = models.FeriasProcessadas
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
    class Table(serializers.ModelSerializer):
        colaborador = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='nome'
        )
        class Meta:
            model = models.FeriasProcessadas
            fields = '__all__'  # Ou liste os campos que deseja expor na API

        
class FeriasUtilizadas(serializers.ModelSerializer):
    class Meta:
        model = models.FeriasUtilizadas
        fields = '__all__'  # Ou liste os campos que deseja expor na API

    class Table(serializers.ModelSerializer):
        colaborador = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='nome'
        )
        class Meta:
            model = models.FeriasUtilizadas
            fields = '__all__'  # Ou liste os campos que deseja expor na API

   
class Insalubridade(serializers.ModelSerializer):
    class Meta:
        model = models.Insalubridade
        fields = '__all__' # Ou liste os campos que deseja expor na API     
   
class Ocupacao(serializers.ModelSerializer):
    class Meta:
        model = models.Ocupacao
        fields = '__all__' # Ou liste os campos que deseja expor na API     
        
class Lembrete(serializers.ModelSerializer):
    
    class Meta:
        model = models.Lembrete
        fields = '__all__' # Ou liste os campos que deseja expor na API     

class Lembrete(serializers.ModelSerializer):
    
    class Meta:
        model = views.Lembrete2
        fields = '__all__' # Ou liste os campos que deseja expor na API     

class Feriado(serializers.ModelSerializer):
    
    class Meta:
        model = models.Feriado
        fields = '__all__' # Ou liste os campos que deseja expor na API     


class Avaliacao(serializers.ModelSerializer):

    class Meta:
        model = models.Colaborador
        fields = '__all__'  # Ou liste os campos que deseja expor na API  

    class Table(serializers.ModelSerializer):
        colab_avaliacao = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='situacao'
        )
        class Meta:
            model = models.Colaborador
            fields = '__all__'  # Ou liste os campos que deseja expor na API  
class HorasPonto(serializers.ModelSerializer):

    class Meta:
        model = models.HorasPonto
        fields = '__all__'  # Ou liste os campos que deseja expor na API  

class TipoAvaliacao(serializers.ModelSerializer):
    class Meta:
        model = models.ColabAvaliacao
        fields = '__all__'  # Ou liste os campos que deseja expor na API  


    class Select(serializers.ModelSerializer):
            value = serializers.CharField(source='id')
            text = serializers.CharField(source='situacao')
            
            class Meta:
                model = models.ColabAvaliacao
                fields = ['value','text']  # Ou liste os campos que deseja expor na API   
        

class IntegracaoNr(serializers.ModelSerializer):
    class Meta:
        model = models.IntegracaoNr
        fields = '__all__' # Ou liste os campos que deseja expor na API
    class Table(serializers.ModelSerializer):
        class Meta:
            model = models.IntegracaoNr 
            fields =  ['id','validade','nr'] # Ou liste os campos que deseja expor na API

class IntegracaoEpi(serializers.ModelSerializer):
    class Meta:
        model = models.IntegracaoEpi
        fields = '__all__' # Ou liste os campos que deseja expor na API
    class Table(serializers.ModelSerializer):
        class Meta:
            model = models.IntegracaoEpi
            fields = ['id','aso','aso_valid','epi','epi_valid','os','os_valid','observacao'] # Ou liste os campos que deseja expor na API

class Integracao(serializers.ModelSerializer):
    class Meta:
        model = models.Integracao
        fields = '__all__' # Ou liste os campos que deseja expor na API
    class Table(serializers.ModelSerializer):
        class Meta:
            model = models.Integracao
            fields = ['id','obra','validade','descricao'] # Ou liste os campos que deseja expor na API


class IntegracaoNrTipo(serializers.ModelSerializer):
    class Meta:
        model = models.IntegracaoNrTipo
        fields = '__all__' # Ou liste os campos que deseja expor na API
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='id')
        class Meta:
            model = models.IntegracaoNrTipo
            fields = ['value','text']
class Obra(serializers.ModelSerializer):
    class Meta:
        model = models.Obra
        fields = '__all__'
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='empresa')
        class Meta:
            model = models.Obra
            fields = ['value','text']

