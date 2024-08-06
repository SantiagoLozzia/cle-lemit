# pylint: disable=import-error
from rest_framework import serializers
from database.models import Presupuesto, DetallePresupuesto, Solicitante, Servicio, DataServicio
import logging

# Configurar el logger
logger = logging.getLogger(__name__)

class DetallePresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePresupuesto
        fields = ['nro_servicio', 'cant', 'subtotal']


class PresupuestoSerializer(serializers.ModelSerializer):
    detalles_presupuesto = DetallePresupuestoSerializer(many=True)

    class Meta:
        model = Presupuesto
        fields = '__all__'
    
    def create(self, validated_data):
        detalles_presupuesto_data = validated_data.pop('detalles_presupuesto', [])
        
        logger.debug("Validated Data: %s", validated_data)
        logger.debug("Detalles Presupuesto Data: %s", detalles_presupuesto_data)
        
        try:
            presupuesto = Presupuesto.objects.create(**validated_data)
        except Exception as e:
            logger.error("Error creating Presupuesto: %s", str(e))
            raise e

        for detalle_data in detalles_presupuesto_data:
            try:
                logger.debug("Detalle Data: %s", detalle_data)
                DetallePresupuesto.objects.create(nro_presupuesto=presupuesto, **detalle_data)
            except Exception as e:
                logger.error("Error creating DetallePresupuesto: %s", str(e))
                raise e
        
        return presupuesto


class PresupuestoEnEsperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presupuesto
        fields = ['nro_presupuesto', 'fecha', 'area_tematica', 'estado_presupuesto']

class SolicitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitante
        fields = ['nro_solicitante', 'nombre_solicitante', 'telefono', 'email']

class SeleccionarSolicitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitante
        fields = ['nro_solicitante', 'nombre_solicitante', 'telefono', 'email'] 

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['nro_servicio', 'servicio', 'norma', 'area_tematica']

class SeleccionarServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['nro_servicio', 'servicio', 'norma', 'area_tematica', 'arancel', 'modulo']

class PresupuestosAceptadosSerializer(serializers.ModelSerializer):
    nombre_solicitante = serializers.CharField(source='nro_solicitante.nombre_solicitante')
    nro_dataServicio = serializers.SerializerMethodField()

    class Meta:
        model = Presupuesto
        fields = ['nro_presupuesto', 'fecha_presupuesto', 'area_tematica', 'estado_presupuesto', 'nombre_solicitante', 'nro_dataServicio']

    def get_nro_dataServicio(self, obj):
        data_servicio = DataServicio.objects.filter(nro_presupuesto=obj).first()
        return data_servicio.nro_dataServicio if data_servicio else None