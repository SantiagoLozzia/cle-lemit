from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MyTokenObtainPairView, NombreYApellidoUser

# Crea un enrutador y regístralo con el UserViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Ruta para obtener el token JWT
    path('authentication/', MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('authentication/user_info/', NombreYApellidoUser.as_view(), name='nombre-y-apellido-user'),

    # Rutas para los usuarios gestionados por el enrutador
    path('users/', include(router.urls)),
]
