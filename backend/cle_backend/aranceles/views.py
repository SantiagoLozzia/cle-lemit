import json
import logging

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.decorators import api_view

from database.models import Servicio, Modulo
from .serializers import ServicioSerializer

logger = logging.getLogger(__name__)


class ServicioListView(generics.ListCreateAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class ServicioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

def obtener_todos_los_aranceles(request):
    aranceles = Servicio.objects.all()  # Obtener todos los aranceles desde la base de datos
    serializer = ServicioSerializer(aranceles, many=True)  # Serializar los aranceles
    return JsonResponse(serializer.data, safe=False)  # Devolver los aranceles en formato JSON

@api_view(['GET'])
def obtener_modulo(request):
    try:
        modulo = Modulo.obtener_ultimo_modulo()  # Obtiene la última instancia de Modulo
        return JsonResponse({'valor': modulo.valor})
    except Modulo.DoesNotExist:
        return JsonResponse({'error': 'No se encontró ningún módulo'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def actualizar_modulo(request):
    rol = getattr(getattr(request.user, 'userprofile', None), 'rol', None)
    if rol not in ('administracion', 'direccion'):
        return JsonResponse({'error': 'No tiene permisos para actualizar el módulo.'}, status=403)

    try:
        nuevo_valor = int(request.data.get('nuevo_valor', 1000))
        Modulo.actualizar_modulo(nuevo_valor)
        modulo = Modulo.obtener_ultimo_modulo()
        return JsonResponse({'mensaje': 'Valor actualizado', 'nuevo_valor': modulo.valor})
    except ValueError:
        return JsonResponse({'error': 'Valor no válido'}, status=400)
    except Exception:
        logger.exception("Error en actualizar_modulo")
        return JsonResponse({'error': 'Error interno del servidor.'}, status=500)

