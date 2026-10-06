from unittest.mock import patch

from django.core.management import call_command, CommandError
from django.test import SimpleTestCase


class CreateSuperuserConfigurationTests(SimpleTestCase):
	def test_missing_credentials_prevent_superuser_creation(self):
		with patch.dict(
			'os.environ',
			{
				'DJANGO_SUPERUSER_USERNAME': '',
				'DJANGO_SUPERUSER_EMAIL': '',
				'DJANGO_SUPERUSER_PASSWORD': '',
			},
		):
			with self.assertRaises(CommandError):
				call_command('create_superusers')
