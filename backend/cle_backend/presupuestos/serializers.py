# pylint: disable=import-error
from rest_framework import serializers
from database.models import Presupuesto, Solicitante, Servicio

class PresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presupuesto
        fields = '__all__'

class SolicitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitante
        fields = ['nro_solicitante', 'nombre_solicitante']

class SeleccionarSolicitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitante
        fields = ['nro_solicitante', 'nombre_solicitante', 'telefono', 'email'] 

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['nro_servicio', 'servicio', 'servicio', 'norma', 'area_tematica']

class SeleccionarServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['nro_servicio', 'servicio', 'servicio', 'norma', 'area_tematica', 'arancel']