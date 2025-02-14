from rest_framework import serializers
from . import models

class Colaborador(serializers.ModelSerializer):
    class Meta:
        model = models.Colaborador
        fields = '__all__'  # Ou liste os campos que deseja expor na API  
        
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='nome')
        text = serializers.CharField(source='nome')
        
        class Meta:
            model = models.Colaborador
            fields = ['value','text']  # Ou liste os campos que deseja expor na API
    def Select_encarregado():
        return Colaborador.Select(models.Colaborador.objects.all().filter(encarregado=True, demissao__isnull=True),many=True).data
    
    class Table(serializers.ModelSerializer):
        admissao = serializers.DateField('%d/%m/%Y')
        class Meta:
            model = models.Colaborador
            fields = '__all__'  # Ou liste os campos que deseja expor na API  
class Obra(serializers.ModelSerializer):
    class Meta:
        model = models.Obra
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.SerializerMethodField()

        class Meta:
            model = models.Obra   
            fields = ['value','text']  # Ou liste os campos que deseja expor na API    

        def get_text(self, obj):
            # Personalize a string combinando os atributos desejados
            return f"{obj.id} || {obj.empresa} - {obj.cidade}"
class Atividade(serializers.ModelSerializer):
    class Meta:
        model = models.Atividade
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        

class Diarioobra(serializers.ModelSerializer):
    class Meta:
        model = models.Diarioobra
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
class Programacao(serializers.ModelSerializer):
    class Meta:
        model = models.Localizacaoprogramada   
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
class Funcao(serializers.ModelSerializer):
    class Meta:
        model = models.Funcao   
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='funcao')
        text = serializers.CharField(source='funcao')
        class Meta:
            model = models.Funcao   
            fields = ['value','text']  # Ou liste os campos que deseja expor na API 
class Supervisor(serializers.ModelSerializer):
    class Meta:
        model = models.Supervisor   
        fields = '__all__'  # Ou liste os campos que deseja expor na API    
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='id')
        class Meta:
            model = models.Supervisor   
            fields = ['value','text']  # Ou liste os campos que deseja expor na API    
class Dia(serializers.ModelSerializer):
    class Meta:
        model = models.Dia   
        fields = '__all__'  # Ou liste os campos que deseja expor na API    
class ValorHora(serializers.ModelSerializer):
    class Meta:
        model = models.ValorHora   
        fields = '__all__'  # Ou liste os campos que deseja expor na API    


class TipoAtividadeSelect(serializers.ModelSerializer):
    
    class Meta:
        model = models.TipoAtividade
        fields = '__all__'  # Ou liste os campos que deseja expor na API    
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='tipo')
        text = serializers.CharField(source='tipo')
        
        class Meta:
            model = models.TipoAtividade
            fields = ['value','text']  # Ou liste os campos que deseja expor na API    