import logging

from rest_framework.permissions import BasePermission, IsAuthenticated  # noqa: F401 — re-exported for convenience

logger = logging.getLogger(__name__)

PRIVILEGED_ROLES = {'servicios_tecnologicos', 'administracion', 'direccion'}

ALLOWED_UPLOAD_MIME_TYPES = {
    'application/pdf',
    'image/jpeg',
    'image/jpg',
    'image/png',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/msword',
    'application/vnd.ms-excel',
}


def get_user_rol(request):
    try:
        return request.user.userprofile.rol
    except AttributeError:
        return None


def get_user_area(request):
    try:
        return request.user.userprofile.area_tematica
    except AttributeError:
        return None


def validate_upload_file(file):
    """Raise ValueError if the uploaded file's MIME type is not in the allowlist."""
    if file is not None and file.content_type not in ALLOWED_UPLOAD_MIME_TYPES:
        raise ValueError('Tipo de archivo no permitido.')


def user_can_access_circuit(user, nro_circuito):
    """Return True if the user is privileged or belongs to the circuit's area."""
    from database.models import DataServicio  # local import avoids circular dependency

    try:
        rol = user.userprofile.rol
    except AttributeError:
        return False

    if rol in PRIVILEGED_ROLES:
        return True

    try:
        ds = DataServicio.objects.select_related('nro_presupuesto').get(
            nro_circuito=nro_circuito
        )
        return ds.nro_presupuesto.area_tematica == user.userprofile.area_tematica
    except DataServicio.DoesNotExist:
        return False


class IsServiciosTecnologicos(BasePermission):
    message = 'Acción restringida a Servicios Tecnológicos.'

    def has_permission(self, request, view):
        return get_user_rol(request) == 'servicios_tecnologicos'


class IsAreaJefe(BasePermission):
    message = 'Acción restringida a Jefes de Área.'

    def has_permission(self, request, view):
        return get_user_rol(request) == 'area_jefe'


class IsDireccion(BasePermission):
    message = 'Acción restringida a Dirección.'

    def has_permission(self, request, view):
        return get_user_rol(request) == 'direccion'


class IsAdministracion(BasePermission):
    message = 'Acción restringida a Administración.'

    def has_permission(self, request, view):
        return get_user_rol(request) == 'administracion'


class IsAdministracionOrDireccion(BasePermission):
    message = 'Acción restringida a Administración o Dirección.'

    def has_permission(self, request, view):
        return get_user_rol(request) in ('administracion', 'direccion')


class IsAreaUser(BasePermission):
    """Jefe o standard de cualquier área temática."""
    message = 'Acción restringida a usuarios de área.'

    def has_permission(self, request, view):
        return get_user_rol(request) in ('area_jefe', 'area_standard')
