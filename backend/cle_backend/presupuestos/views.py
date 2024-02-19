from rest_framework import generics
from database.models import Presupuesto, Solicitante, Servicio
from .serializers import PresupuestoSerializer, SolicitanteSerializer, SeleccionarSolicitanteSerializer, ServicioSerializer, SeleccionarServicioSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

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