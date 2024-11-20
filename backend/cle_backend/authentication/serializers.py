from rest_framework import serializers
from django.contrib.auth.models import User
from database.models import UserProfile, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['area_tematica', 'rol']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    # Puedes utilizar un método de validación para asegurarte de que el perfil siempre esté presente
    def validate(self, attrs):
        user = self.instance or self.initial_data
        if not hasattr(user, 'userprofile'):
            raise serializers.ValidationError("UserProfile is required.")
        return attrs

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadir información personalizada al token
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['role'] = user.userprofile.rol
        token['area_tematica'] = user.userprofile.area_tematica

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Añadir información personalizada a la respuesta del serializer
        data['role'] = self.user.userprofile.rol 
        data['area_tematica'] = self.user.userprofile.area_tematica
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name

        return data