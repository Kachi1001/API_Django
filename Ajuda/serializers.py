from rest_framework import serializers
from . import models

class Menu(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = '__all__'  # Ou liste os campos que deseja expor na API  
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.SerializerMethodField()

        class Meta:
            model = models.Menu
            fields = ['value','text']  # Ou liste os campos que deseja expor na API    
        def get_text(self, obj):
            return f"{obj.app.nome  } - {obj.nome}"
    class Table(serializers.ModelSerializer):
        app = serializers.SlugRelatedField( many=False, read_only= True,slug_field='nome')
        class Meta:
            model = models.Menu
            fields = ['id','app','nome']  # Ou liste os campos que deseja expor na API    
        
class Submenu(serializers.ModelSerializer):
    class Meta:
        model = models.Submenu
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
        
class App(serializers.ModelSerializer):
    class Meta:
        model = models.App
        fields = '__all__'  # Ou liste os campos que deseja expor na API
    class Select(serializers.ModelSerializer):
        value = serializers.CharField(source='id')
        text = serializers.CharField(source='nome')

        class Meta:
            model = models.App
            fields = ['value','text']  # Ou liste os campos que deseja expor na API    