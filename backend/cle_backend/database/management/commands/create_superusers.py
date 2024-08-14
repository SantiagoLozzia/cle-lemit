from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Crea un superusuario con la información proporcionada'

    def handle(self, *args, **kwargs):
        username = 'santiago_lozzia'
        email = 'santiagolozzia@gmail.com'
        password = 'rootsantiago'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superusuario {username} creado con éxito.'))
        else:
            self.stdout.write(self.style.WARNING(f'El superusuario {username} ya existe.'))
