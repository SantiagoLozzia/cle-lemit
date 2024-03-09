from rest_framework import generics
from database.models import Presupuesto, Solicitante, Servicio
from .serializers import PresupuestoSerializer, SolicitanteSerializer, SeleccionarSolicitanteSerializer, ServicioSerializer, SeleccionarServicioSerializer, PresupuestoEnEsperaSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, api_view
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

class PresupuestoListView(generics.ListCreateAPIView):
    queryset = Presupuesto.objects.all()
    serializer_class = PresupuestoSerializer

class PresupuestoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Presupuesto.objects.all()
    serializer_class = PresupuestoSerializer

def obtener_todos_los_presupuestos(request):
    presupuestos = Presupuesto.objects.all()  # Obtener todos los presupuestos desde la base de datos
    serializer = PresupuestoSerializer(presupuestos, many=True)  # Serializar los presupuestos
    return JsonResponse(serializer.data, safe=False)  # Devolver los presupuestos en formato JSON

@require_http_methods(["GET"])
def presupuestos_enEspera(request):
    presupuestos = Presupuesto.objects.filter(estado_presupuesto='en_espera').select_related('nro_solicitante')
    
    # Ahora cada presupuesto en la lista debería tener el nombre del solicitante
    presupuestos_con_solicitante = []
    for presupuesto in presupuestos:
        presupuesto_dict = {
            'nro_presupuesto': presupuesto.nro_presupuesto,
            'fecha_presupuesto': presupuesto.fecha_presupuesto,
            'area_tematica': presupuesto.area_tematica,
            'estado_presupuesto': presupuesto.estado_presupuesto,
            'nombre_solicitante': presupuesto.nro_solicitante.nombre_solicitante  
        }
        presupuestos_con_solicitante.append(presupuesto_dict)
    
    return JsonResponse(presupuestos_con_solicitante, safe=False)

@require_http_methods(["GET"])
def presupuestos_cancelados(request):
    presupuestos = Presupuesto.objects.filter(
                                                Q(estado_presupuesto='rechazado') |
                                                Q(estado_presupuesto='modificado') |
                                                Q(estado_presupuesto='actualizado')
                                            ).select_related('nro_solicitante')
    
    # Ahora cada presupuesto en la lista debería tener el nombre del solicitante
    presupuestos_con_solicitante = []
    for presupuesto in presupuestos:
        presupuesto_dict = {
            'nro_presupuesto': presupuesto.nro_presupuesto,
            'fecha_presupuesto': presupuesto.fecha_presupuesto,
            'area_tematica': presupuesto.area_tematica,
            'estado_presupuesto': presupuesto.estado_presupuesto,
            'nombre_solicitante': presupuesto.nro_solicitante.nombre_solicitante  
        }
        presupuestos_con_solicitante.append(presupuesto_dict)
    
    return JsonResponse(presupuestos_con_solicitante, safe=False)

@api_view(['PUT'])
def actualizar_estado_presupuesto(request, nro_presupuesto):
    try:
        presupuesto = Presupuesto.objects.get(nro_presupuesto=nro_presupuesto)
        nuevo_estado = request.data.get('estado_presupuesto')

        if nuevo_estado in ['en_espera', 'rechazado', 'modificado', 'actualizado']:
            presupuesto.estado_presupuesto = nuevo_estado
            presupuesto.save()

            return JsonResponse({'mensaje': 'Estado del presupuesto actualizado correctamente'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'mensaje': 'El estado proporcionado no es válido'}, status=status.HTTP_400_BAD_REQUEST)

    except Presupuesto.DoesNotExist:
        return JsonResponse({'mensaje': 'El presupuesto no existe'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return JsonResponse({'mensaje': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def buscar_solicitantes(request):
    term = request.GET.get('q', '')
    solicitantes = Solicitante.objects.filter(nombre_solicitante__icontains=term)
    serializer = SolicitanteSerializer(solicitantes, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def seleccionar_solicitante(request, nro_solicitante):
    try:
        solicitante = get_object_or_404(Solicitante, nro_solicitante=nro_solicitante)
        serializer = SeleccionarSolicitanteSerializer(solicitante, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def buscar_servicios(request):
    term = request.GET.get('q', '')
    servicios = Servicio.objects.filter(servicio__icontains=term)
    serializer = ServicioSerializer(servicios, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def seleccionar_servicio(request, nro_servicio):
    try:
        servicio = get_object_or_404(Servicio, nro_servicio=nro_servicio)
        serializer = SeleccionarServicioSerializer(servicio, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)