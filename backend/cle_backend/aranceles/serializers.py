# pylint: disable=import-error
from rest_framework import serializers
from database.models import Servicio

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'