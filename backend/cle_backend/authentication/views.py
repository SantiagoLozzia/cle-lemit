from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('userprofile')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class NombreYApellidoUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "first_name": user.first_name,
            "last_name": user.last_name
        })
    
class FirmaUsuario(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.userprofile
        if profile.firma:
            url = request.build_absolute_uri(profile.firma.url)
            return Response({'tiene_firma': True, 'firma_url': url})
        return Response({'tiene_firma': False, 'firma_url': None})

    def post(self, request):
        archivo = request.FILES.get('firma')
        if not archivo:
            return Response({'error': 'Archivo requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        profile = request.user.userprofile
        if profile.firma:
            profile.firma.delete(save=False)
        profile.firma = archivo
        profile.save()
        url = request.build_absolute_uri(profile.firma.url)
        return Response({'tiene_firma': True, 'firma_url': url})

    def delete(self, request):
        profile = request.user.userprofile
        if profile.firma:
            profile.firma.delete(save=False)
            profile.firma = None
            profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

