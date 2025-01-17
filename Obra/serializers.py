from rest_framework import serializers
from . import models

        
        
class Obra(serializers.ModelSerializer):
    class Meta:
        model = models.Obra
        fields = '__all__'
    class Select():
        class depto(serializers.ModelSerializer):
            value = serializers.CharField(source='id')
            text = serializers.SerializerMethodField()
            
            class Meta:
                model = models.Obra
                fields = ['value', 'text']

            def get_text(self, obj):
                # Personalize a string combinando os atributos desejados
                return f"{obj.cliente} || {obj.cidade} - {obj.orcamento}"
        class almox(serializers.ModelSerializer):
            value = serializers.CharField(source='id')
            text = serializers.SerializerMethodField()
            
            class Meta:
                model = models.Obra
                fields = ['value', 'text']

            def get_text(self, obj):
                # Personalize a string combinando os atributos desejados
                return f"{obj.id} || {obj.cliente} - {obj.cidade}"
Select = {
    'obra': {
        'depto': Obra.Select.depto(models.Obra.objects.all().order_by('cliente'), many=True).data,
        'almox': Obra.Select.almox(models.Obra.objects.all().order_by('id'),many=True).data,
    },
}    