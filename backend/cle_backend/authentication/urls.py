from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, MyTokenObtainPairView, NombreYApellidoUser,
    FirmaUsuario, LeyendaUsuario,
    PerfilUsuario, ChangePassword, ForgotPassword, ResetPassword,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('user_info/', NombreYApellidoUser.as_view(), name='nombre-y-apellido-user'),
    path('firma_usuario/', FirmaUsuario.as_view(), name='firma-usuario'),
    path('leyenda_usuario/', LeyendaUsuario.as_view(), name='leyenda-usuario'),
    path('perfil/', PerfilUsuario.as_view(), name='perfil-usuario'),
    path('change_password/', ChangePassword.as_view(), name='change-password'),
    path('forgot_password/', ForgotPassword.as_view(), name='forgot-password'),
    path('reset_password/', ResetPassword.as_view(), name='reset-password'),
    path('users/', include(router.urls)),
]
