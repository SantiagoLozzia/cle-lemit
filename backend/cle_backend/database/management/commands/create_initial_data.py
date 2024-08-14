from django.core.management.base import BaseCommand
from django.core.management import call_command, CommandError

class Command(BaseCommand):
    help = 'Configura todos los roles y usuarios predeterminados'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando configuración de roles y usuarios...'))

        try:
            # Primero, crea los grupos necesarios
            call_command('create_administracion')
            call_command('create_area_jefe')
            call_command('create_area_standard')
            call_command('create_direccion')
            call_command('create_servicios_tecnologicos')

            # Luego, crea los superusuarios
            call_command('create_superusers')

            # Finalmente, crea los usuarios normales
            call_command('create_users')

        except CommandError as e:
            self.stdout.write(self.style.ERROR(f'Error al ejecutar comandos: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('Roles y usuarios configurados correctamente.'))
