from rest_framework import serializers

import Obra.models
from . import models

from Depto_pessoal import serializers as depto
from Obra import serializers as obra     
        
class Produto(serializers.ModelSerializer):
    class Meta:
        model = models.Produto
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='produto')
        
        class Meta:
            model = models.Produto  
            fields = ['value', 'text']  # Ou liste os campos que deseja expor na API 

class EpiCadastro(serializers.ModelSerializer):
    class Meta:
        model = models.EpiCadastro
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.SerializerMethodField()
        
        class Meta:
            model = models.EpiCadastro
            fields = ['value', 'text','produto']

        def get_text(self, obj):
            # Personalize a string combinando os atributos desejados
            return f"{obj.id} | CA {obj.ca} | {obj.tamanho} | {obj.fabricante}"
            
    class Table(serializers.ModelSerializer):
        produto = Produto(
            many=False,
            read_only=True,
        )
        class Meta:
            model = models.EpiCadastro
            fields = '__all__'  # Ou liste os campos que deseja expor na API
            
class EpiMovimentacao(serializers.ModelSerializer):
    class Meta:
        model = models.EpiMovimentacao
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='id')
        
        class Meta:
            model = models.EpiMovimentacao
            fields = ['value', 'text']  # Ou liste os campos que deseja expor na API 
    class Table(serializers.ModelSerializer):
        epi_cadastro = EpiCadastro.Table(many=False,read_only=True)
        class Meta:
            model = models.EpiMovimentacao
            fields = '__all__'  # Ou liste os campos que deseja expor na API
class Numeracao(serializers.ModelSerializer):
    class Meta:
        model = models.Numeracao
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='id')
        
        class Meta:
            model = models.Numeracao
            fields = ['value', 'text']  # Ou liste os campos que deseja expor na API 
    class Table(serializers.ModelSerializer):
        colaborador = serializers.SerializerMethodField()
        class Meta:
            model = models.Numeracao
            fields = '__all__'  # Ou liste os campos que deseja expor na API
    
        def get_colaborador(self, obj):
            colabs = depto.Colaborador.objects.all()
            return f"{colabs.get(id=obj.colaborador).nome}"
class Ficha(serializers.ModelSerializer):
    class Meta:
        model = models.Ficha
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.SerializerMethodField()
        class Meta:
            model = models.Ficha
            fields = ['value', 'text','colaborador']  # Ou liste os campos que deseja expor na API 
        def get_text(self, obj):
            comp = 'Completa' if obj.completa else 'Incompleta'
            return f"Página - {obj.pagina} | {comp}" 
    class Table(serializers.ModelSerializer):
        colaborador = serializers.SerializerMethodField()
        class Meta:
            model = models.Ficha
            fields = ['id','colaborador','pagina','completa']  # Ou liste os campos que deseja expor na API

        def get_colaborador(self, obj):
            colabs = depto.Colaborador.objects.all()
            return f"{colabs.get(id=obj.colaborador).nome}"
    class Almoxarifado():
        def select():
            class Select(serializers.ModelSerializer):
                value = serializers.CharField(source='id')
                text = serializers.SerializerMethodField()
                
                class Meta:
                    model = models.Obra
                    fields = ['value', 'text']

                def get_text(self, obj):
                    # Personalize a string combinando os atributos desejados
                    return f"{obj.id} || {obj.cliente} - {obj.cidade}"
class Obra(serializers.ModelSerializer):
    class Meta:
        from Obra.models import Obra   
        model = Obra
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.SerializerMethodField()
        
        class Meta:
            from Obra.models import Obra   
            model = Obra
            fields = ['value', 'text']

        def get_text(self, obj):
            # Personalize a string combinando os atributos desejados
            return f"{obj.id} || {obj.cliente} - {obj.cidade}"
class Colaborador(serializers.ModelSerializer):
    class Meta:
        from Depto_pessoal.models import Colaborador
        model = Colaborador
        fields = '__all__'  # Ou liste os campos que deseja expor na API  
           

    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='nome')

        class Meta:
            from Depto_pessoal.models import Colaborador
            model = Colaborador
            fields = ['value','text','ativo']  # Ou liste os campos que deseja expor na API    

Select = {
    'obra': Obra.Select,
    'colaborador': Colaborador.Select,
    'epi_movimentacao': EpiMovimentacao.Select,
    'epi_cadastro': EpiCadastro.Select,
    'produto': Produto.Select,
    'ficha': Ficha.Select,
}    
Table = {
    'epi_cadastro': EpiCadastro.Table,
    'epi_movimentacao': EpiMovimentacao.Table
}