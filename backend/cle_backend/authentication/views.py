import os
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
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

    def _get_profile(self, user):
        from database.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile

    def get(self, request):
        profile = self._get_profile(request.user)
        if profile.firma:
            url = request.build_absolute_uri(profile.firma.url)
            return Response({'tiene_firma': True, 'firma_url': url})
        return Response({'tiene_firma': False, 'firma_url': None})

    def post(self, request):
        archivo = request.FILES.get('firma')
        if not archivo:
            return Response({'error': 'Archivo requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        profile = self._get_profile(request.user)
        if profile.firma:
            profile.firma.delete(save=False)
        profile.firma = archivo
        profile.save()
        url = request.build_absolute_uri(profile.firma.url)
        return Response({'tiene_firma': True, 'firma_url': url})

    def delete(self, request):
        profile = self._get_profile(request.user)
        if profile.firma:
            profile.firma.delete(save=False)
            profile.firma = None
            profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LeyendaUsuario(APIView):
    permission_classes = [IsAuthenticated]

    def _get_profile(self, user):
        from database.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile

    def get(self, request):
        profile = self._get_profile(request.user)
        return Response({'leyenda': profile.leyenda or ''})

    def post(self, request):
        leyenda = request.data.get('leyenda', '').strip()
        profile = self._get_profile(request.user)
        profile.leyenda = leyenda
        profile.save(update_fields=['leyenda'])
        return Response({'leyenda': profile.leyenda})


class PerfilUsuario(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })

    def put(self, request):
        user = request.user
        user.first_name = request.data.get('first_name', user.first_name).strip()
        user.last_name = request.data.get('last_name', user.last_name).strip()
        email = request.data.get('email', user.email).strip()
        user.email = email
        user.save(update_fields=['first_name', 'last_name', 'email'])
        return Response({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current = request.data.get('current_password', '')
        new_pw = request.data.get('new_password', '')
        if not request.user.check_password(current):
            return Response({'error': 'Contraseña actual incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(new_pw) < 8:
            return Response({'error': 'La nueva contraseña debe tener al menos 8 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(new_pw)
        request.user.save()
        return Response({'ok': True})


class ForgotPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        # Siempre responder OK para no revelar si el email existe
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({'ok': True})

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:8080')
        reset_link = f'{frontend_url}/reset-password?uid={uid}&token={token}'

        send_mail(
            subject='Restablecer contraseña — CLE LEMIT',
            message=(
                f'Hola {user.first_name or user.username},\n\n'
                f'Recibimos una solicitud para restablecer tu contraseña.\n'
                f'Hacé clic en el siguiente enlace para elegir una nueva:\n\n'
                f'{reset_link}\n\n'
                f'Si no solicitaste este cambio, podés ignorar este mensaje.\n'
                f'El enlace expira en 24 horas.\n\n'
                f'CLE LEMIT'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response({'ok': True})


class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get('uid', '')
        token = request.data.get('token', '')
        new_password = request.data.get('new_password', '')

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Enlace inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'El enlace expiró o ya fue usado.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({'error': 'La contraseña debe tener al menos 8 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'ok': True})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
