from rest_framework import serializers
from . import models

class SerializerTipo(serializers.Serializer):
    integer_field = serializers.IntegerField()
    string_field = serializers.CharField(max_length=200)
    boolean_field = serializers.BooleanField()

    def validate_integer_field(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Este campo precisa ser um número.")
        return value

    def validate_string_field(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Este campo precisa ser um texto.")
        return value

    def validate_boolean_field(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("Este campo precisa ser verdadeiro ou falso.")
        return value


class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Colaborador
        fields = '__all__'  # Ou liste os campos que deseja expor na API  
        

        
class ObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Obra
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Atividade
        fields = '__all__'  # Ou liste os campos que deseja expor na API
class DiarioobraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Diarioobra
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
class ProgramacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Localizacaoprogramada   
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
class FuncaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Funcao   
        fields = '__all__'  # Ou liste os campos que deseja expor na API

class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Supervisor   
        fields = '__all__'  # Ou liste os campos que deseja expor na API    

# Select
class FuncaoSelect(serializers.ModelSerializer):
    value = serializers.CharField(source='funcao')
    text = serializers.CharField(source='funcao')
    class Meta:
        model = models.Funcao   
        fields = ['value','text']  # Ou liste os campos que deseja expor na API 
           
class SupervisorSelect(serializers.ModelSerializer):
    value = serializers.CharField(source='supervisor')
    text = serializers.CharField(source='supervisor')
    class Meta:
        model = models.Supervisor   
        fields = ['value','text']  # Ou liste os campos que deseja expor na API    

class ObraSelect(serializers.ModelSerializer):
    value = serializers.CharField(source='id')
    text = serializers.SerializerMethodField()

    class Meta:
        model = models.Obra   
        fields = ['value','text']  # Ou liste os campos que deseja expor na API    

    def get_text(self, obj):
        # Personalize a string combinando os atributos desejados
        return f"{obj.id} || {obj.empresa} - {obj.cidade}"
    
class ColaboradorSelect(serializers.ModelSerializer):
    value = serializers.CharField(source='nome')
    text = serializers.CharField(source='nome')
    
    class Meta:
        model = ColaboradorSerializer.Meta.model
        fields = ['value','text']  # Ou liste os campos que deseja expor na API    

class TipoAtividadeSelect(serializers.ModelSerializer):
    value = serializers.CharField(source='tipo')
    text = serializers.CharField(source='tipo')
    
    class Meta:
        model = models.TipoAtividade
        fields = ['value','text']  # Ou liste os campos que deseja expor na API    
        
 

Select = {
    'funcao': FuncaoSelect,
    'supervisor': SupervisorSelect,
    'obra': ObraSelect,
    'colaborador': ColaboradorSelect,
    'atividade': TipoAtividadeSelect,
    'indice': [{'text':'ATESTADO'},{'text':'DISPENSAS E FOLGAS'},{'text':'FALTAS'},{'text':'FÉRIAS'},{'text':'OBRAS ENGENHARIA'},{'text':'RETRABALHOS'},{'text':'SERVIÇOS INTERNOS'},{'text':'SERVIÇOS INTERNOS'}, {'text':'TREINAMENTO'},{'text':'SERVIÇOS PARA O GRUPO'}],
    'encarregado': ColaboradorSelect(models.Colaborador.objects.all().filter(encarregado=True, demissao__isnull=True),many=True).data
}    