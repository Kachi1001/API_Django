from rest_framework import serializers

from . import models, views
        
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
    def Select_ordened():
        return Produto.Select(Produto.Select.Meta.model.objects.all().order_by('produto'), many=True).data

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
            return f"{obj.id} | {('CA ' + obj.ca) if obj.ca != 'S/CA' else obj.ca} | {obj.fabricante}"
            
    class Table(serializers.ModelSerializer):
        produto = serializers.SlugRelatedField(many=False,read_only=True, slug_field='produto')
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
        colabs = {}
        queyset = models.Colaborador.objects.all().values()
        for colab in queyset:
            colabs[colab['id']] = colab
        colaborador = serializers.SerializerMethodField()
        epi_cadastro = EpiCadastro.Table(many=False,read_only=True)
        produto = serializers.SlugRelatedField(many=False,read_only=True, slug_field='produto')
        ficha = serializers.SlugRelatedField(many=False,read_only=True, slug_field='pagina')
        
        class Meta:
            model = models.EpiMovimentacao
            fields = '__all__'  # Ou liste os campos que deseja expor na API
        def get_colaborador(self, obj):
            return self.colabs.get(obj.colaborador)
        
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
            colabs = models.Colaborador.objects.all()
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
    def Select_ordened():
        classe = Ficha.Select
        return classe(classe.Meta.model.objects.all().order_by('-pagina'), many=True).data
    class Table(serializers.ModelSerializer):
        colaborador = serializers.SerializerMethodField()
        class Meta:
            model = models.Ficha
            fields = ['id','colaborador','pagina','completa']  # Ou liste os campos que deseja expor na API

        def get_colaborador(self, obj):
            colabs = models.Colaborador.objects.all()
            return f"{colabs.get(id=obj.colaborador).nome}"
        
class FichaPadrao(serializers.ModelSerializer):
    class Meta:
        model = models.FichaPadrao
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Table(serializers.ModelSerializer):
        produto = serializers.SlugRelatedField(many=False,read_only=True, slug_field='produto')
        class Meta:
            model = models.FichaPadrao
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
            fields = ['value', 'text']

        def get_text(self, obj):
            # Personalize a string combinando os atributos desejados
            return f"{obj.id} || {obj.empresa} - {obj.cidade}"
class Colaborador(serializers.ModelSerializer):
    class Meta:
        model =  models.Colaborador
        fields = '__all__'  # Ou liste os campos que deseja expor na API  
           

    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='nome')

        class Meta:
            model = models.Colaborador
            fields = ['value','text','ativo']  # Ou liste os campos que deseja expor na API    
    def Select_ordened():
        return Colaborador.Select(Colaborador.Select.Meta.model.objects.all().order_by('nome'), many=True).data

class EpisValidos():
    class Table(serializers.ModelSerializer):
        class Meta:
            model = views.EpisValidos
            fields = '__all__'  # Ou liste os campos que deseja expor na API

class Erros(serializers.ModelSerializer):
    class Meta:
        model = models.Erros
        fields = '__all__'  # Ou liste os campos que deseja expor na API
Select = {
    'obra': Obra.Select,
    'colaborador': Colaborador.Select_ordened,
    'epi_movimentacao': EpiMovimentacao.Select,
    'epi_cadastro': EpiCadastro.Select,
    'produto': Produto.Select_ordened,
    'ficha': Ficha.Select_ordened,
}    
Table = {
    'epi_cadastro': EpiCadastro.Table,
    'epi_movimentacao': EpiMovimentacao.Table
}