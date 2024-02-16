from rest_framework import generics
from database.models import Presupuesto, Solicitante
from .serializers import PresupuestoSerializer, SolicitanteSerializer
from django.http import JsonResponse

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
    # Obtener el término de búsqueda del parámetro de la URL
    term = request.GET.get('term', '')

    # Realizar la búsqueda en la base de datos
    solicitantes = Solicitante.objects.filter(nombre__icontains=term)

    # Serializar los resultados
    serializer = SolicitanteSerializer(solicitantes, many=True)

    # Devolver los resultados en formato JSON
    return JsonResponse(serializer.data, safe=False)