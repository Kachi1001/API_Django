from rest_framework import serializers
from .models import *

class CarrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carros
        fields = '__all__'  # Ou liste os campos que deseja expor na API

class AgendaSalasSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendaSalas
        fields = '__all__'  # Ou liste os campos que deseja expor na API

