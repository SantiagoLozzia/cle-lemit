from rest_framework import generics
from database.models import Solicitante
from .serializers import SolicitanteSerializer
from django.http import JsonResponse

class SolicitanteListView(generics.ListCreateAPIView):
    queryset = Solicitante.objects.all()
    serializer_class = SolicitanteSerializer

class SolicitanteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Solicitante.objects.all()
    serializer_class = SolicitanteSerializer

def obtener_todos_los_solicitantes(request):
    solicitantes = Solicitante.objects.all()  # Obtener todos los solicitantes desde la base de datos
    serializer = SolicitanteSerializer(solicitantes, many=True)  # Serializar los solicitantes
    return JsonResponse(serializer.data, safe=False)  # Devolver los solicitantes en formato JSON
