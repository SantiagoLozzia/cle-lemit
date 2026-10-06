from unittest.mock import patch

from channels.testing import WebsocketCommunicator
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from cle_backend.asgi import application
from cle_backend.middleware import APIJWTAuthenticationMiddleware
from authentication.views import UserViewSet


class ProtectedAPIView(APIView):
	def get(self, request):
		return Response({'ok': True})


class APIJWTAuthenticationMiddlewareTests(SimpleTestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.get_response = lambda request: HttpResponse('ok')
		self.middleware = APIJWTAuthenticationMiddleware(self.get_response)

	def test_api_request_without_bearer_token_is_rejected(self):
		response = self.middleware(self.factory.get('/api/encurso/'))

		self.assertEqual(response.status_code, 401)

	def test_invalid_token_is_rejected(self):
		request = self.factory.get('/api/encurso/', HTTP_AUTHORIZATION='Bearer invalid')
		with patch('cle_backend.middleware.JWTAuthentication') as jwt_authentication:
			jwt_authentication.return_value.get_validated_token.side_effect = AuthenticationFailed
			response = self.middleware(request)

		self.assertEqual(response.status_code, 401)

	def test_valid_token_sets_authenticated_user(self):
		request = self.factory.get('/api/encurso/', HTTP_AUTHORIZATION='Bearer valid')
		user = object()
		with patch('cle_backend.middleware.JWTAuthentication') as jwt_authentication:
			jwt_authentication.return_value.get_validated_token.return_value = object()
			jwt_authentication.return_value.get_user.return_value = user
			response = self.middleware(request)

		self.assertEqual(request.user, user)
		self.assertEqual(response.status_code, 200)

	def test_login_and_explicit_lookup_paths_remain_public(self):
		paths = (
			'/api/auth/',
			'/api/presupuestos/seleccionar_solicitante/1/',
			'/api/presupuestos/seleccionar_servicio/1/',
		)

		for path in paths:
			with self.subTest(path=path):
				response = self.middleware(self.factory.get(path))
				self.assertEqual(response.status_code, 200)

	def test_other_authentication_routes_are_not_public(self):
		response = self.middleware(self.factory.get('/api/auth/users/'))

		self.assertEqual(response.status_code, 401)

	def test_non_api_request_is_not_intercepted(self):
		response = self.middleware(self.factory.get('/admin/'))

		self.assertEqual(response.status_code, 200)


class DRFPermissionDefaultsTests(SimpleTestCase):
	def test_drf_api_views_require_authentication_by_default(self):
		response = ProtectedAPIView.as_view()(APIRequestFactory().get('/'))

		self.assertEqual(response.status_code, 401)


class UserManagementPermissionTests(SimpleTestCase):
	def test_user_management_is_staff_only(self):
		self.assertEqual(UserViewSet.permission_classes, [IsAdminUser])


class WebSocketAuthenticationTests(SimpleTestCase):
	@override_settings(CHANNEL_LAYERS={'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}})
	async def test_connection_without_jwt_subprotocol_is_rejected(self):
		communicator = WebsocketCommunicator(
			application,
			'/ws/mi_canal/',
			headers=[(b'host', b'localhost'), (b'origin', b'http://localhost')],
		)

		connected, close_message = await communicator.connect()

		self.assertFalse(connected)
		self.assertEqual(close_message, 4401)

	@override_settings(CHANNEL_LAYERS={'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}})
	async def test_valid_jwt_subprotocol_authenticates_before_group_join(self):
		communicator = WebsocketCommunicator(
			application,
			'/ws/mi_canal/',
			headers=[(b'host', b'localhost'), (b'origin', b'http://localhost')],
			subprotocols=['jwt', 'valid'],
		)

		with patch('cle_backend.consumers.get_user_from_token') as get_user:
			async def authenticated_user(token):
				return object()

			get_user.side_effect = authenticated_user
			connected, subprotocol = await communicator.connect()
			self.assertTrue(connected)
			self.assertEqual(subprotocol, 'jwt')
			self.assertEqual(
				await communicator.receive_json_from(),
				{'message': 'Conexión WebSocket establecida'},
			)
			await communicator.disconnect()

	@override_settings(CHANNEL_LAYERS={'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}})
	async def test_invalid_jwt_subprotocol_is_rejected(self):
		communicator = WebsocketCommunicator(
			application,
			'/ws/mi_canal/',
			headers=[(b'host', b'localhost'), (b'origin', b'http://localhost')],
			subprotocols=['jwt', 'invalid'],
		)

		with patch(
			'cle_backend.consumers.get_user_from_token',
			side_effect=AuthenticationFailed,
		):
			connected, close_message = await communicator.connect()

		self.assertFalse(connected)
		self.assertEqual(close_message, 4401)

	@override_settings(CHANNEL_LAYERS={'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}})
	async def test_untrusted_origin_is_rejected(self):
		communicator = WebsocketCommunicator(
			application,
			'/ws/mi_canal/',
			headers=[(b'host', b'localhost'), (b'origin', b'http://attacker.invalid')],
			subprotocols=['jwt', 'valid'],
		)

		connected, _ = await communicator.connect()

		self.assertFalse(connected)
