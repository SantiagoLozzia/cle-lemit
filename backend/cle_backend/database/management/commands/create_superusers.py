from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Crea un superusuario con la información proporcionada'

    def handle(self, *args, **kwargs):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', '').strip()
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '').strip()
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
        if not username or not email or not password:
            raise CommandError(
                'Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and '
                'DJANGO_SUPERUSER_PASSWORD before creating the superuser.'
            )

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superusuario {username} creado con éxito.'))
        else:
            self.stdout.write(self.style.WARNING(f'El superusuario {username} ya existe.'))
