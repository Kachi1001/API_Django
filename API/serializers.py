from rest_framework import serializers
from .models import *

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
        model = Colaborador
        fields = '__all__'  # Ou liste os campos que deseja expor na API     
        
class ObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obra
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        
class LancamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lancamentos
        fields = '__all__'  # Ou liste os campos que deseja expor na API

class CarrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carros
        fields = '__all__'  # Ou liste os campos que deseja expor na API
