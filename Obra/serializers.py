from rest_framework import serializers
from . import models

        
        
class Obra(serializers.ModelSerializer):
    class Meta:
        model = models.Obra
        fields = '__all__'
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='id')
        
        class Meta:
            model = models.Obra
            fields = ['text','value']
Select = {
    'obra': Obra.Select,
}    