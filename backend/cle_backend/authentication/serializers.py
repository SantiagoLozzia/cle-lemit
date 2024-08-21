from rest_framework import serializers
from django.contrib.auth.models import User
from database.models import UserProfile, UserProfile

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
