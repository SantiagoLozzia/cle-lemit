from rest_framework import generics
from database.models import Servicio
from .serializers import ServicioSerializer
from django.http import JsonResponse

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