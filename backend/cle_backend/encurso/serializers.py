from rest_framework import serializers
from database.models import DataServicio, Presupuesto, DetallePresupuesto, Solicitante, Servicio

class NroPresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presupuesto
        fields = ['nro_presupuesto']

class DataServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataServicio
        fields = ['fecha', 'obra', 'muestras', 'plazo_estimado', 'cant_numLabs', 'nro_presupuesto', 'nro_presupuesto']

class PresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presupuesto
        fields = ['area_tematica']

class ObtenerServiciosEnCursoSerializer(serializers.ModelSerializer):
    # Define el campo para area_tematica directamente
    area_tematica = serializers.CharField(source='nro_presupuesto.area_tematica')

    class Meta:
        model = DataServicio
        fields = ['nro_dataServicio', 'fecha', 'nro_presupuesto', 'area_tematica', 'adjunto_solicitudServicio', 'completo']

class GuardarAdjuntoSolicitudDataServicioSerializer(serializers.ModelSerializer):
    class Meta:
            model = DataServicio
            fields = ['nro_dataServicio', 'adjunto_solicitudServicio']