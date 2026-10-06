import re

from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class APIJWTAuthenticationMiddleware:
    public_api_paths = {'/api/auth/'}
    public_api_patterns = (
        re.compile(r'^/api/presupuestos/seleccionar_solicitante/\d+/$'),
        re.compile(r'^/api/presupuestos/seleccionar_servicio/\d+/$'),
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/') and request.method != 'OPTIONS':
            is_public = request.path in self.public_api_paths or any(
                pattern.fullmatch(request.path) for pattern in self.public_api_patterns
            )
            if not is_public:
                authorization = get_authorization_header(request).split()
                if len(authorization) != 2 or authorization[0].lower() != b'bearer':
                    return JsonResponse(
                        {'detail': 'Authentication credentials were not provided.'},
                        status=401,
                    )

                try:
                    jwt_authentication = JWTAuthentication()
                    token = jwt_authentication.get_validated_token(authorization[1])
                    request.user = jwt_authentication.get_user(token)
                except AuthenticationFailed:
                    return JsonResponse(
                        {'detail': 'Invalid authentication credentials.'},
                        status=401,
                    )

        return self.get_response(request)