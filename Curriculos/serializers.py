from rest_framework import serializers
from . import models, views
from Site_django import util
        
        

class Candidato(serializers.ModelSerializer):
    class Meta:
        model = models.Candidato
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.SerializerMethodField()
        class Meta:
            model = models.Candidato
            fields = ['value', 'text']  # Ou liste os campos que deseja expor na API 
    
        def get_text(self, obj):
            return f"{obj.nome}  -  rg: {obj.rg or 'Vazio'} | cpf: {obj.cpf or 'Vazio'}"
    def Select_ordened():   
        return util.Select_order_by(Candidato.Select, 'nome')
class Escolaridade(serializers.ModelSerializer):
    class Meta:
        model = models.Escolaridade
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        
        class Meta:
            model = models.EscolaridadeTipo
            fields = '__all__'  # Ou liste os campos que deseja expor na API
            
    def Select_ordened():   
        return Escolaridade.Select(models.EscolaridadeTipo.objects.all().order_by('indice'), many=True).data
    
class Experiencia(serializers.ModelSerializer):
    class Meta:
        model = models.Experiencia
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Table(serializers.ModelSerializer):
        area_atuacao = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='area'
        )
        area_atuacao_sub = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='sub_area'
        )
        class Meta:
            model = models.Experiencia
            fields = ['id','candidato','area_atuacao','area_atuacao_sub','empresa','data_inicio','data_fim','tempo_anos','data_cadastro','revisar'] # Ou liste os campos que deseja expor na API
        
class Questionario(serializers.ModelSerializer):
    class Meta:
        model = models.Questionario
        fields = '__all__'  # Ou li\\ste os campos que deseja expor na API
class Percepcao(serializers.ModelSerializer):
    class Meta:
        model = models.Percepcao
        fields = '__all__'  # Ou li\\ste os campos que deseja expor na API

        
        
class Profissoes(serializers.ModelSerializer):
    class Meta:
        model = models.Profissoes
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='funcao')
        class Meta:
            model = models.Profissoes
            fields =  ['value','text']  # Ou liste os campos que deseja expor na API7
    def Select_ordened():
        response = Profissoes.Select(models.Profissoes.objects.all().order_by('funcao'), many=True).data
        return response
    
class Entrevista(serializers.ModelSerializer):
    class Meta:
        model = models.Entrevista
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='id')

        class Meta:
            model = models.Entrevista
            fields =  ['value','text']  # Ou liste os campos que deseja expor na API
class Cnh(serializers.ModelSerializer):
    class Meta:
        model = models.Cnh
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        class Meta:
            model = models.Cnh
            fields = ['value']  # Ou liste os campos que deseja expor na API 
class EstadoCivil(serializers.ModelSerializer):
    class Meta:
        model = models.EstadoCivil
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        class Meta:
            model = models.EstadoCivil
            fields = ['value']  # Ou liste os campos que deseja expor na API 
    
class AvaliacaoTipo(serializers.ModelSerializer):
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        class Meta:
            model = models.AvaliacaoTipo
            fields = ['value']  # Ou liste os campos que deseja expor na API 
        
class Entrevista_classificacao(serializers.ModelSerializer):
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        class Meta:
            model = models.EntrevistaClassificacao
            fields = ['value']  # Ou liste os campos que deseja expor na API 
            
            
class Setor(serializers.ModelSerializer):
    class Meta:
        model = models.Setor
        fields = '__all__'  # Ou liste os campos que deseja expor na API 
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='setor')
        class Meta:
            model = models.Setor
            fields = ['value','text']
            
class Anexos(serializers.ModelSerializer):
    class Meta:
        model = models.Anexos
        fields = '__all__'  # Ou liste os campos que deseja expor na API  


class IndicacaoColaboradores():
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='nome')
        class Meta:
            from Depto_pessoal.models import Colaborador
            model = Colaborador
            fields = ['value']
            
class Estado(serializers.ModelSerializer):
    class Meta:
        model = models.Estado
        fields = '__all__'  # Ou liste os campos que deseja expor na API  

    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='nome')
        class Meta:
            model = models.Estado
            fields = ['value','text']
    def Select_ordened(): 
        return util.Select_order_by(Estado.Select, 'nome')
    
class AreaAtuacao(serializers.ModelSerializer):
    class Meta:
        model = models.AreaAtuacao
        fields = '__all__'  # Ou liste os campos que deseja expor na API 
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='area')
        class Meta:
            model = models.AreaAtuacao
            fields = ['value','text']
    def Select_ordened():   
        return util.Select_order_by(AreaAtuacao.Select, 'area')
        

class AreaAtuacaoSub(serializers.ModelSerializer):
    class Meta:
        model = models.AreaAtuacaoSub
        fields = '__all__'  # Ou liste os campos que deseja expor na API 
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='sub_area')
        class Meta: 
            model = models.AreaAtuacaoSub
            fields = ['value','text']
    def Select_ordened():   
        return AreaAtuacaoSub.Select(models.AreaAtuacaoSub.objects.all().order_by('sub_area'), many=True).data
    
    class Table(serializers.ModelSerializer):
        area_atuacao = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='area'
        )
        class Meta:
            model = models.AreaAtuacaoSub
            fields = '__all__'  # Ou liste os campos que deseja expor na API
            
class Classificacao(serializers.ModelSerializer):
    class Meta:
        model = models.Classificacao
        fields = '__all__'  # Ou liste os campos que deseja expor na API 
    class Table(serializers.ModelSerializer):
        setor = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='setor'
        )
        area_atuacao = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='area'
        )
        class Meta:
            model = models.Classificacao
            fields = '__all__'  # Ou liste os campos que deseja expor na API
class Indicacoes(serializers.ModelSerializer):
    class Meta:
        model = models.Indicacoes
        fields = '__all__'
    class Table(serializers.ModelSerializer):
        candidato = serializers.SlugRelatedField(many=False, read_only=True, slug_field='nome')
        data_recebimento = serializers.DateField('%d/%m/%Y')
        data_finalizacao = serializers.DateField('%d/%m/%Y')
        class Meta:
            model = models.Indicacoes
            fields = '__all__'
class IndicacoesExternas(serializers.ModelSerializer):
    class Meta:
        model = views.IndicacoesExternas
        fields = '__all__'
    class Table(serializers.ModelSerializer):
        data_recebimento = serializers.DateField('%d/%m/%Y')
        data_finalizacao = serializers.DateField('%d/%m/%Y')
        class Meta:
            model = views.IndicacoesExternas
            fields = '__all__'
