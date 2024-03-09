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
class RecepcionEnCursoSerializer(serializers.ModelSerializer):
     class Meta:
        model = Recepcion
        fields = '__all__'
     
class OrdenServicioEmCursoSerializer(serializers.ModelSerializer):
     class Meta:
        model = OrdenServicio
        fields = '__all__'

class InformeAreaEnCursoSerializer(serializers.ModelSerializer):
     class Meta:   
        model = InformeArea
        fields = '__all__'

class InformeServicioEnCursoSerializer(serializers.ModelSerializer):
     class Meta:
        model = InformeArea
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