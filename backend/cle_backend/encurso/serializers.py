from rest_framework import serializers
from database.models import *

class NroPresupuestoSerializer(serializers.ModelSerializer):
        class Meta:
                model = Presupuesto
                fields = ['nro_presupuesto']

class DataServicioSerializer(serializers.ModelSerializer):
        class Meta:
                model = DataServicio
                fields = '__all__'

class PresupuestoSerializer(serializers.ModelSerializer):
        class Meta:
                model = Presupuesto
                fields = '__all__'

class SolicitanteSerializer(serializers.ModelSerializer):
        class Meta:
                model = Solicitante
                fields = '__all__'

class LegajoEnCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legajo
        fields = '__all__'
    
class GuardarPagoLegajoSerializer(serializers.ModelSerializer):
        class Meta:
                model = Legajo
                fields = ['pago']

class CambiarPlazoPagoSerializer(serializers.ModelSerializer):
        class Meta:
                model = Legajo
                fields = ['plazo_pago']

class RecepcionEnCursoSerializer(serializers.ModelSerializer):
        class Meta:
                model = Recepcion
                fields = '__all__'
        
class OrdenServicioEnCursoSerializer(serializers.ModelSerializer):
        class Meta:
                model = OrdenServicio
                fields = '__all__'

class DetallePresupuestoSerializer(serializers.ModelSerializer):
        servicio = serializers.CharField(source='nro_servicio.servicio')

        class Meta:
                model = DetallePresupuesto
                fields = ['nro_servicio', 'servicio', 'cant']

class InformeAreaParcialEnCursoSerializer(serializers.ModelSerializer):
        class Meta:   
                model = InformeAreaParcial
                fields = '__all__'

class InformeAreaEnCursoSerializer(serializers.ModelSerializer):
        informes_parciales = InformeAreaParcialEnCursoSerializer(many=True, read_only=True)
        
        class Meta:   
                model = InformeArea
                fields = '__all__'

class InformeServicioEnCursoSerializer(serializers.ModelSerializer):
        class Meta:
                model = InformeServicio
                fields = '__all__'
        
class SolicitudInterAreaEnCursoSerializer(serializers.ModelSerializer):
        class Meta:
                model = SolicitudInterarea
                fields = '__all__'
                
class InformeInterAreaEnCursoSerializer(serializers.ModelSerializer):
        class Meta:
                model = InformeInterarea
                fields = '__all__'


class GuardarAdjuntoSolicitudDataServicioSerializer(serializers.ModelSerializer):
        class Meta:
                model = DataServicio
                fields = ['nro_dataServicio', 'adjunto_solicitudServicio']


class GuardarAdjuntoFacturaSerializer(serializers.ModelSerializer):
        class Meta:
                model = Legajo
                fields = ['nro_legajo', 'adjunto_factura']


class CambiarRemitoSerializer(serializers.ModelSerializer):
        class Meta:
                model = Recepcion
                fields = ['nros_remitos']

class GuardarEstadoMuestrasSerializer(serializers.ModelSerializer):
        class Meta:
                model = Recepcion
                fields = ['estado_recepcion']

class CambiarPlazoMuestrasSerializer(serializers.ModelSerializer):
        class Meta:
                model = Recepcion
                fields = ['plazo_muestras']

class CambiarPlazoEstimadoSerializer(serializers.ModelSerializer):
        class Meta:
                model = DataServicio
                fields = ['plazo_estimado']

class GuardarAdjuntoInformeArea(serializers.ModelSerializer):
        class Meta:
                model = InformeArea
                fields = ['']

class GuardarRegistrosEnsayoServicioSerializer(serializers.ModelSerializer):
        class Meta:
                model = InformeArea
                fields = '__all__'

class SolicitudInterareaSerializer(serializers.ModelSerializer):
        class Meta:
                model = SolicitudInterarea
                fields = '__all__'

class DetalleInterareaSerializer(serializers.ModelSerializer):
    servicio = serializers.SerializerMethodField()
    
    class Meta:
        model = DetalleInterarea
        fields = ('nro_servicio', 'cant', 'servicio')
    
    def get_servicio(self, obj):
        # Obtener el nombre del servicio usando el nro_servicio
        servicio = Servicio.objects.get(pk=obj.nro_servicio.pk)
        return servicio.servicio
    
class InformeInterareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformeInterarea
        fields = '__all__'

class InformeServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformeServicio
        fields = '__all__'

class CorregirInformeServicioSerializer(serializers.ModelSerializer):
        class Meta:
                model = InformeServicio
                fields = ['corregir']

class AdvertirCorreccionesSerializer(serializers.ModelSerializer):
       class Meta:
                model = InformeServicio
                fields = ('correcciones', 'corregir', 'revision')

                
class CambiarRevision(serializers.ModelSerializer):
       class Meta:
        model = InformeServicio
        fields = '__all__'