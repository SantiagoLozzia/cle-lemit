# pylint: disable=import-error
from rest_framework import serializers
from database.models import Solicitante

class SolicitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitante
        fields = '__all__'
