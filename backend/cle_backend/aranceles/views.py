from rest_framework import generics
from database.models import Servicio, Modulo
from .serializers import ServicioSerializer
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, api_view
import json


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

@csrf_exempt
@api_view(['POST'])
def actualizar_modulo(request):
    if request.method == 'POST':
        try:
            nuevo_valor = int(request.data.get('nuevo_valor', 1000))
            Modulo.actualizar_modulo(nuevo_valor)
            modulo = Modulo.obtener_ultimo_modulo()
            return JsonResponse({'mensaje': 'Valor actualizado', 'nuevo_valor': modulo.valor})
        except ValueError:
            return JsonResponse({'error': 'Valor no válido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

