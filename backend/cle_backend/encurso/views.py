from django.shortcuts import render
from .serializers import *
from database.models import *
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

class ObtenerTodoEnCurso(APIView):
    def get(self, request, format=None):
        # Obtener todos los DataServicio donde DataServicio.finalizado = False
        servicios_en_curso = DataServicio.objects.filter(finalizado=False)

        # Obtener el numero de presupuesto de los DataServicio
        numeros_presupuesto = servicios_en_curso.values_list('nro_presupuesto', flat=True)

        # Obtener el área temática de cada presupuesto
        areas_tematicas = Presupuesto.objects.filter(nro_presupuesto__in=numeros_presupuesto) \
                                               .values('nro_presupuesto', 'area_tematica')

        # Crear un diccionario para mapear el número de presupuesto con su área temática
        presupuesto_map = {presupuesto['nro_presupuesto']: presupuesto['area_tematica'] 
                           for presupuesto in areas_tematicas}

        # Serializar los datos de los DataServicio
        servicios_en_curso_serializer = DataServicioSerializer(servicios_en_curso, many=True)

        # Agregar el campo 'area_tematica' a los datos de DataServicio
        for data_servicio in servicios_en_curso_serializer.data:
            nro_presupuesto = data_servicio['nro_presupuesto']
            data_servicio['area_tematica'] = presupuesto_map.get(nro_presupuesto, '')

        # Obtener el numero de circuito de los DataServicio
        numeros_circuito = servicios_en_curso.values_list('nro_circuito', flat=True)

        # Obtener los datos de los otros modelos
        legajos = Legajo.objects.filter(nro_circuito__in=numeros_circuito)
        recepciones = Recepcion.objects.filter(nro_circuito__in=numeros_circuito)
        ordenes_servicio = OrdenServicio.objects.filter(nro_circuito__in=numeros_circuito)
        informes_area = InformeArea.objects.filter(nro_circuito__in=numeros_circuito)
        informes_servicio = InformeServicio.objects.filter(nro_circuito__in=numeros_circuito)
        solicitudes_inter_area = SolicitudInterarea.objects.filter(nro_circuito__in=numeros_circuito)
        informes_inter_area = InformeInterarea.objects.filter(nro_circuito__in=numeros_circuito)

        # Serializar los datos
        legajos_serializer = LegajoEnCursoSerializer(legajos, many=True)
        recepciones_serializer = RecepcionEnCursoSerializer(recepciones, many=True)
        ordenes_servicio_serializer = OrdenServicioEmCursoSerializer(ordenes_servicio, many=True)
        informes_area_serializer = InformeAreaEnCursoSerializer(informes_area, many=True)
        informes_servicio_serializer = InformeServicioEnCursoSerializer(informes_servicio, many=True)
        solicitudes_inter_area_serializer = SolicitudInterAreaEnCursoSerializer(solicitudes_inter_area, many=True)
        informes_inter_area_serializer = InformeInterAreaEnCursoSerializer(informes_inter_area, many=True)

        # Construir la respuesta
        response_data = {
            'solicitudes': servicios_en_curso_serializer.data,
            'legajos': legajos_serializer.data,
            'recepciones': recepciones_serializer.data,
            'ordenes_servicio': ordenes_servicio_serializer.data,
            'informes_area': informes_area_serializer.data,
            'informes_servicio': informes_servicio_serializer.data,
            'solicitudes_inter_area': solicitudes_inter_area_serializer.data,
            'informes_inter_area': informes_inter_area_serializer.data
        }

        # Devolver la respuesta
        return Response(response_data)


class GuardarAdjuntoSolicitud(APIView):
    def post(self, request):
        nro_dataServicio = request.data.get('nroDataServicio')
        data_servicio = DataServicio.objects.get(nro_dataServicio=nro_dataServicio)
        adjunto = request.FILES.get('archivo')
        data_servicio.adjunto_solicitudServicio = adjunto
        data_servicio.save()
        serializer = GuardarAdjuntoSolicitudDataServicioSerializer(data_servicio)
        return Response(serializer.data, status=status.HTTP_200_OK)

