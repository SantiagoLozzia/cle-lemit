from django.shortcuts import render
from .serializers import NroPresupuestoSerializer, DataServicioSerializer, ObtenerServiciosEnCursoSerializer, PresupuestoSerializer, GuardarAdjuntoSolicitudDataServicioSerializer
from database.models import DataServicio, Presupuesto, DetallePresupuesto, Solicitante, Servicio, Circuito
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class NrosPresupuestoEnEspera(APIView):
    def get(self, request):
        # Filtrar los presupuestos con estado 'en_espera'
        numeros_presupuesto = Presupuesto.objects.filter(estado_presupuesto='en_espera') \
            .annotate(nombre_solicitante=F('nro_solicitante__nombre_solicitante')) \
            .values('nro_presupuesto', 'nombre_solicitante') \
            .order_by('nro_presupuesto')

        data = list(numeros_presupuesto)

        return Response(data)

def presupuesto_seleccionado(request, nro_presupuesto):
    try:
        presupuesto = Presupuesto.objects.select_related('nro_solicitante').get(nro_presupuesto=nro_presupuesto)
        # Obtiene el nombre del solicitante asociado al presupuesto
        nombre_solicitante = presupuesto.nro_solicitante.nombre_solicitante
        
        # Construye el diccionario de datos a devolver
        data = {
            'nro_presupuesto': presupuesto.nro_presupuesto,
            'nombre_solicitante': nombre_solicitante,
        }
        return JsonResponse(data)
    except Presupuesto.DoesNotExist:
        return JsonResponse({'error': 'Presupuesto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
class GuardarDataServicioView(APIView):
    def post(self, request, *args, **kwargs):
        # Crear una instancia de Circuito
        circuito_instance = Circuito.objects.create()

        # Crear una instancia de DataServicio utilizando la clave primaria del Circuito
        data_servicio_data = request.data
        data_servicio_data['nro_circuito'] = circuito_instance.pk
        data_servicio_serializer = DataServicioSerializer(data=data_servicio_data)

        if data_servicio_serializer.is_valid():
            data_servicio_instance = data_servicio_serializer.save()

            # Obtener el número de presupuesto del DataServicio
            nro_presupuesto = data_servicio_data.get('nro_presupuesto')

            # Actualizar el estado del presupuesto asociado
            try:
                presupuesto = Presupuesto.objects.get(nro_presupuesto=nro_presupuesto)
                presupuesto.estado_presupuesto = 'aceptado'  # Cambiar aquí al estado deseado
                presupuesto.save()
            except Presupuesto.DoesNotExist:
                pass  # Manejar el caso donde no se encuentra el presupuesto

            return Response(data_servicio_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data_servicio_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObtenerServiciosEnCurso(APIView):
    def get(self, request, format=None):
        # Obtener todos los servicios en curso
        servicios_en_curso = DataServicio.objects.all()

        # Serializar los servicios en curso con información de presupuesto
        serializer = ObtenerServiciosEnCursoSerializer(servicios_en_curso, many=True)

        # Devolver la respuesta con los datos serializados
        return Response(serializer.data, status=status.HTTP_200_OK)

class GuardarAdjuntoSolicitud(APIView):
    def post(self, request):
        nro_dataServicio = request.data.get('nroDataServicio')
        data_servicio = DataServicio.objects.get(nro_dataServicio=nro_dataServicio)
        adjunto = request.FILES.get('archivo')
        data_servicio.adjunto_solicitudServicio = adjunto
        data_servicio.save()
        serializer = GuardarAdjuntoSolicitudDataServicioSerializer(data_servicio)
        return Response(serializer.data, status=status.HTTP_200_OK)

