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

class InformeInterAreaEnCursoSerializer(serializers.ModelSerializer):
        class Meta:
                model = InformeInterarea
                fields = '__all__'

class AdjuntoSolicitudServicioSerializer(serializers.ModelSerializer):
        class Meta:
                model = AdjuntoSolicitudServicio
                fields = ['id', 'data_servicio', 'archivo', 'fecha']

class AdjuntoFacturaSerializer(serializers.ModelSerializer):
        class Meta:
                model = AdjuntoFactura
                fields = ['id', 'legajo', 'archivo', 'monto', 'fecha']

class RegistroEnsayoCicloSerializer(serializers.ModelSerializer):
        class Meta:
                model = RegistroEnsayoCiclo
                fields = ['id', 'ciclo', 'archivo', 'fecha']

class CorreccionSerializer(serializers.ModelSerializer):
        class Meta:
                model = Correccion
                fields = ['id', 'tipo', 'destinatario', 'descripcion', 'fecha', 'estado', 'autor']

class CicloInformeSerializer(serializers.ModelSerializer):
        registros_ensayo = RegistroEnsayoCicloSerializer(many=True, read_only=True)
        historial_correcciones = CorreccionSerializer(many=True, read_only=True)

        class Meta:
                model = CicloInforme
                fields = '__all__'

class RegistroEnsayoCicloIASerializer(serializers.ModelSerializer):
        class Meta:
                model = RegistroEnsayoCicloIA
                fields = '__all__'

class CorreccionIASerializer(serializers.ModelSerializer):
        class Meta:
                model = CorreccionIA
                fields = ['id', 'tipo', 'destinatario', 'descripcion', 'fecha', 'estado', 'autor']

class CicloInterareaSerializer(serializers.ModelSerializer):
        registros_ensayo = RegistroEnsayoCicloIASerializer(many=True, read_only=True)
        historial_correcciones = CorreccionIASerializer(many=True, read_only=True)

        class Meta:
                model = CicloInterarea
                fields = '__all__'

class SolicitudInterAreaEnCursoSerializer(serializers.ModelSerializer):
        ciclos = CicloInterareaSerializer(many=True, read_only=True)

        class Meta:
                model = SolicitudInterarea
                fields = '__all__'

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
        servicio = Servicio.objects.get(pk=obj.nro_servicio.pk)
        return servicio.servicio

class InformeInterareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformeInterarea
        fields = '__all__'

class CorregirCicloSerializer(serializers.ModelSerializer):
        class Meta:
                model = CicloInforme
                fields = ['corregir']

class AdvertirCorreccionesCicloSerializer(serializers.ModelSerializer):
        class Meta:
                model = CicloInforme
                fields = ['correcciones', 'corregir', 'revision_confirmada']

class EventoAuditoriaSerializer(serializers.ModelSerializer):
        usuario_nombre = serializers.SerializerMethodField()

        class Meta:
                model = EventoAuditoria
                fields = ['id', 'accion', 'descripcion', 'fecha', 'nro_circuito', 'usuario_nombre']

        def get_usuario_nombre(self, obj):
                if obj.usuario:
                        nombre = f"{obj.usuario.first_name} {obj.usuario.last_name}".strip()
                        return nombre if nombre else obj.usuario.username
                return 'Sistema'
