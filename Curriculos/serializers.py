from rest_framework import serializers
from .models import *

        
        

class Candidato(serializers.ModelSerializer):
    class Meta:
        model = Candidato
        fields = '__all__'  # Ou liste os campos que deseja expor na API
        

Select = {
        'candidato': Candidato,
}    