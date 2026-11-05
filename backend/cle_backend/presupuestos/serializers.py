# pylint: disable=import-error
from rest_framework import serializers
from database.models import Presupuesto, DetallePresupuesto, Solicitante, Servicio, DataServicio, ConfigFormulario
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

        # Snapshot: capturar versión vigente del formulario al momento de creación
        if not validated_data.get('version_formulario'):
            try:
                config = ConfigFormulario.objects.get(tipo='presupuesto')
                validated_data['version_formulario'] = config.version_actual
            except ConfigFormulario.DoesNotExist:
                validated_data['version_formulario'] = '01'

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
    nro_legajo = serializers.SerializerMethodField()

    class Meta:
        model = Presupuesto
        fields = ['nro_presupuesto', 'fecha_presupuesto', 'area_tematica', 'estado_presupuesto', 'nombre_solicitante', 'nro_dataServicio', 'nro_legajo']

    def get_nro_dataServicio(self, obj):
        data_servicio = DataServicio.objects.filter(nro_presupuesto=obj).first()
        return data_servicio.nro_dataServicio if data_servicio else None

    def get_nro_legajo(self, obj):
        data_servicio = DataServicio.objects.select_related('nro_circuito__legajo').filter(nro_presupuesto=obj).first()
        if data_servicio and data_servicio.nro_circuito:
            try:
                return data_servicio.nro_circuito.legajo.nro_legajo
            except Exception:
                return None
        return None