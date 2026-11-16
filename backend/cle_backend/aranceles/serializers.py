# pylint: disable=import-error
from rest_framework import serializers
from database.models import Servicio, ConceptoFacturacion

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class ConceptoFacturacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptoFacturacion
        fields = ['id', 'nombre']