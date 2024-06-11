# pylint: disable=import-error
from rest_framework import serializers
from database.models import Presupuesto, DetallePresupuesto, Solicitante, Servicio
import logging

# Configurar el logger
logger = logging.getLogger(__name__)

class DetallePresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePresupuesto
        fields = ['nro_servicio', 'cant', 'subtotal']

class PresupuestoSerializer(serializers.ModelSerializer):
    detalles_presupuesto = DetallePresupuestoSerializer(many=True, source="detallepresupuesto_set")

    class Meta:
        model = Presupuesto
        fields = ['fecha_presupuesto', 'contacto', 'telefono2', 'email2', 'area_tematica', 'subtotal', 'descuento', 'arancel_presupuesto', 'observaciones', 'estado_presupuesto', 'nro_solicitante', 'detalles_presupuesto']
    
    def create(self, validated_data):
        # breakpoint()
        detalles_presupuesto_data = validated_data.pop('detalles_presupuesto', [])
        
        # Convertir subtotal y cant a números si son cadenas
        validated_data['subtotal'] = float(validated_data.get('subtotal', 0))
        validated_data['descuento'] = float(validated_data.get('descuento', 0))
        validated_data['arancel_presupuesto'] = float(validated_data.get('arancel_presupuesto', 0))
        
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
                # Convertir subtotal y cant a números si son cadenas
                detalle_data['subtotal'] = float(detalle_data.get('subtotal', 0))
                detalle_data['cant'] = int(detalle_data.get('cant', 0))
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
        fields = ['nro_solicitante', 'nombre_solicitante']

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