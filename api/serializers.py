from rest_framework import serializers
from .models import Topico, Parroquia

class TopicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topico
        fields = ['codigo', 'nombre', 'descripcion']

class ParroquiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parroquia
        fields = ['codigo', 'nombre', 'descripcion']