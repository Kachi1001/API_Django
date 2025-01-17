from rest_framework import serializers
from . import models

        
        

class Candidato(serializers.ModelSerializer):
    class Meta:
        model = models.Candidato
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='nome')
        class Meta:
            model = models.Candidato
            fields = ['value', 'text']  # Ou liste os campos que deseja expor na API 
        
class Escolaridade(serializers.ModelSerializer):
    class Meta:
        model = models.Escolaridade
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        
        class Meta:
            model = models.EscolaridadeTipo
            fields = '__all__'  # Ou liste os campos que deseja expor na API
            
class Experiencia(serializers.ModelSerializer):
    class Meta:
        model = models.Experiencia
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Table(serializers.ModelSerializer):
        profissao = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='funcao'
        )
        candidato = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='nome'
        )
        class Meta:
            model = models.Experiencia
            fields = '__all__'  # Ou liste os campos que deseja expor na API
        
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
            fields =  ['value','text']  # Ou liste os campos que deseja expor na API
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
            
            
class Grupo(serializers.ModelSerializer):
    class Meta:
        model = models.Grupo
        fields = '__all__'  # Ou liste os campos que deseja expor na API 
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='grupo')
        class Meta:
            model = models.Grupo
            fields = ['value','text']
            
class Anexos(serializers.ModelSerializer):
    class Meta:
        model = models.Anexos
        fields = '__all__'  # Ou liste os campos que deseja expor na API  


class Indicacao():
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='nome')
        class Meta:
            from Depto_pessoal.models import Colaborador
            model = Colaborador
            fields = ['value']
            
class Estado():
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='nome')
        class Meta:
            model = models.Estados
            fields = ['value','text']
            
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
        
class Classificacao(serializers.ModelSerializer):
    class Meta:
        model = models.Classificacao
        fields = '__all__'  # Ou liste os campos que deseja expor na API 
    class Table(serializers.ModelSerializer):
        grupo = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='grupo'
        )
        area_atuacao = serializers.SlugRelatedField(
            many=False,
            read_only=True,
            slug_field='area'
        )
        class Meta:
            model = models.Classificacao
            fields = '__all__'  # Ou liste os campos que deseja expor na API

Select = {
    'candidato': Candidato.Select,
    'cnh': Cnh.Select,
    'estado_civil': EstadoCivil.Select,
    'escolaridade': Escolaridade.Select(models.EscolaridadeTipo.objects.all().order_by('indice'), many=True).data,
    'profissao': Profissoes.Select(models.Profissoes.objects.all().order_by('funcao'), many=True).data,
    'banco_talentos': Entrevista_classificacao.Select,
    'grupo': Grupo.Select,
    'indicacao': Indicacao.Select,
    'estado': Estado.Select,
    'area_atuacao': AreaAtuacao.Select
}    